import os
import shlex
import subprocess
import tempfile
import shutil

from django.template.defaultfilters import slugify


from documents.utils import from_descriptor_to_tempfile

from converter.conf.settings import CONVERT_PATH
from converter.conf.settings import OCR_OPTIONS
from converter.conf.settings import DEFAULT_OPTIONS
from converter.conf.settings import LOW_QUALITY_OPTIONS
from converter.conf.settings import HIGH_QUALITY_OPTIONS

#from converter.conf.settings import UNOCONV_PATH

from converter import TEMPORARY_DIRECTORY


QUALITY_DEFAULT = 'quality_default'
QUALITY_LOW = 'quality_low'
QUALITY_HIGH = 'quality_high'

QUALITY_SETTINGS = {QUALITY_DEFAULT:DEFAULT_OPTIONS, QUALITY_LOW:LOW_QUALITY_OPTIONS,
    QUALITY_HIGH:HIGH_QUALITY_OPTIONS}

class ConvertError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message

def cleanup(filename):
    ''' tries to remove the given filename. Ignores non-existent files '''
    try:
        os.remove(filename)
    except OSError:
        pass

def get_errors(error_string):
    '''
    returns all lines in the error_string that start with the string "error"

    '''
    lines = error_string.splitlines()
    return lines[0]
    #error_lines = (line for line in lines if line.find('error') >= 0)
    #return '\n'.join(error_lines)


#TODO: Timeout & kill child
def execute_convert(input_filepath, arguments, output_filepath, quality=QUALITY_DEFAULT):
    command = []
    command.append(CONVERT_PATH)
    command.extend(shlex.split(str(QUALITY_SETTINGS[quality])))
    command.append(input_filepath)
    command.extend(shlex.split(str(arguments)))
    command.append(output_filepath)

    proc = subprocess.Popen(command, stderr=subprocess.PIPE)
    return (proc.wait(), proc.stderr.read())

def execute_unoconv(input_filepath, output_filepath, arguments=''):
    command = [UNOCONV_PATH]
    command.extend(['--stdout'])
    command.extend(shlex.split(str(arguments)))
    command.append(input_filepath)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    with open(output_filepath, 'w') as output:
        shutil.copyfileobj(proc.stdout, output)
    return (proc.wait(), proc.stderr.read())


def cache_cleanup(input_filepath, size, page=0, format='jpg'):
    filepath = create_image_cache_filename(input_filepath, size, page, format)
    try:
        os.remove(filepath)
    except OSError:
        pass
        

def create_image_cache_filename(input_filepath, quality=QUALITY_DEFAULT, *args, **kwargs):
    if input_filepath:
        temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
        temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)

        final_filepath = []
        [final_filepath.append(str(arg)) for arg in args]
        final_filepath.extend(['%s_%s' % (key, value) for key, value in kwargs.items()])
        final_filepath.append(QUALITY_SETTINGS[quality])
        
        temp_path += slugify('_'.join(final_filepath))

        return temp_path
    else:
        return None
   
def in_image_cache(input_filepath, size, page=0, format='jpg', quality=QUALITY_DEFAULT):
    output_filepath = create_image_cache_filename(input_filepath, size=size, page=page, format=format, quality=quality)
    if os.path.exists(output_filepath):
        return output_filepath
    else:
        return None
    
    
def convert(input_filepath, size, quality=QUALITY_DEFAULT, cache=True, page=0, format='jpg', mimetype=None, extension=None):
    unoconv_output = None
    output_filepath = create_image_cache_filename(input_filepath, size=size, page=page, format=format, quality=quality)
    if os.path.exists(output_filepath):
        return output_filepath
    '''
    if extension:
        if extension.lower() == 'ods':
            unoconv_output = '%s_pdf' % output_filepath
            status, error_string = execute_unoconv(input_filepath, unoconv_output, arguments='-f pdf')
            if status:
                errors = get_errors(error_string)
                raise ConvertError(status, errors)            
            cleanup(input_filepath)
            input_filepath = unoconv_output
    '''
    #TODO: Check mimetype and use corresponding utility
    try:
        input_arg = '%s[%s]' % (input_filepath, page)
        status, error_string = execute_convert(input_arg, '-resize %s' % size, '%s:%s' % (format, output_filepath), quality=quality)
        if status:
            errors = get_errors(error_string)
            raise ConvertError(status, errors)
    finally:
        cleanup(input_filepath)
        if unoconv_output:
            cleanup(unoconv_output)
        return output_filepath
    

#TODO: slugify OCR_OPTIONS and add to file name to cache
def convert_document_for_ocr(document, page=0, format='tif'):
    #Extract document file
    document.file.open()
    desc = document.file.storage.open(document.file.path)
    input_filepath = from_descriptor_to_tempfile(desc, document.uuid)
        
    #Convert for OCR
    temp_filename, separator = os.path.splitext(os.path.basename(input_filepath))
    temp_path = os.path.join(TEMPORARY_DIRECTORY, temp_filename)
    output_arg = '%s_ocr%s%s%s' % (temp_path, page, os.extsep, format)
    input_arg = '%s[%s]' % (input_filepath, page)
    try:
        status, error_string = execute_convert(input_arg, OCR_OPTIONS, output_arg)
        if status:
            errors = get_errors(error_string)
            raise ConvertError(status, errors)
    finally:
        return output_arg
