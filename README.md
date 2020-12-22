# EDMS based on DOCUMIUM EDMS

Versionnement de documents.

Stockez plusieurs versions d'un même document, téléchargez ou revenez à une version précédente.

## Signatures numériques.

Vérifier l'authenticité des documents en vérifiant leurs signatures cryptographiques intégrées ou télécharger des signatures détachées pour les documents signés après leur stockage.

## Outils de collaboration.

Discutez des documents ou commentez les nouvelles versions d'un document.

## Métadonnées de documents définies par l'utilisateur.

Plusieurs champs de métadonnées peuvent être associés à un type de document selon des exigences techniques, juridiques ou structurelles telles que le Dublin Core.

Les champs de métadonnées peuvent avoir une valeur initiale, qui peut être statique ou déterminée par un extrait de code modèle fourni par l'utilisateur.

## Les documents peuvent être téléchargés à partir de différentes sources.

Téléchargement de fichiers locaux ou de fichiers côté serveur, copieur multifonctionnel, ou même par courrier électronique.

Téléchargement par lots.

De nombreux documents peuvent être téléchargés en une seule action.

Clonez les métadonnées d'un document pour accélérer les téléchargements et éliminer les saisies répétitives de données.

## Prévisualisation de nombreux formats de fichiers.

L'EDMS permet de générer des aperçus d'images pour de nombreux formats de fichiers courants.

## Prise en charge des formats de documents de bureau.

L'EDMS peut détecter la présence de Libre Office et l'utiliser pour prendre en charge les fichiers de traitement de texte, les feuilles de calcul et les présentations.

## Recherche dans le texte intégral.

Les documents peuvent être recherchés par leur contenu textuel, leurs métadonnées ou tout autre attribut de fichier tel que le nom, l'extension, etc.

## Regroupement de documents configurable.

Liaison automatique des documents sur la base des valeurs des métadonnées ou des propriétés du document.

## Système de contrôle d'accès avancé.

Contrôle d'accès basé sur les rôles. Il est possible de créer un nombre illimité de rôles différents ne se limitant pas au paradigme traditionnel de l'administrateur, de l'opérateur, de l'invité.

Il existe une autorisation pour chaque opération atomique effectuée par les utilisateurs.

## Prise en charge des documents multi-pages.

Les fichiers PDF et TIFF de plusieurs pages sont pris en charge.

## Traitement OCR automatique.

La tâche de transcription du texte des documents par OCR peut être répartie entre plusieurs ordinateurs physiques ou virtuels afin de réduire la charge et d'augmenter la disponibilité.

La langue actuelle du document est transmise au moteur OCR correspondant afin d'augmenter le taux de reconnaissance du texte.

## Interface utilisateur multilingue.

La solution peut être traduite dans pratiquement toutes les langues parlées dans le monde. 

## Backends de stockage enfichables.

Il est très facile d'utiliser des plugins tiers tels que ceux disponibles pour Amazon EC2.

## Balises à code couleur.

Des étiquettes et des codes de couleur peuvent être attribués pour une reconnaissance intuitive.

## Flux de travail.

Gardez une trace de l'état des documents, ainsi que le journal des changements d'état précédents.

#  Run the environment services

```bash
sudo systemctl enable supervisor
sudo systemctl restart supervisor
```

## Or Run through virtual env
```bash
source /opt/mayan-edms/bin/activate
```
In this case, you'll need to create the initial database which in development defaults to an SQLite database. SQLite is a single file database system. Execute:
```bash
./manage.py initialsetup
```

```bash
./manage.py runserver
```

## Use preparestatic instead of collect static
```bash
./manage.py preparestatic
```