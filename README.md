# topo2fantoir

## Contexte, besoin

Vous utilisez un outil qui a besoin d'un fichier au format
[FANTOIR](https://fr.wikipedia.org/wiki/FANTOIR), et ce dernier n'est plus
produit depuis juillet 2023 / a été remplacé par le fichier
[TOPO](https://www.data.gouv.fr/fr/datasets/fichier-des-entites-topographiques-topo-dgfip-1/).
Mais votre outil n'a pas encore été mis à jour pour supporter ce nouveau
fichier.. (ex [plugin qgis cadastre](https://github.com/3liz/QgisCadastrePlugin/issues/345)).

Ce bout de python **essaie** de 'recréer' un fichier départemental FANTOIR depuis
l'export CSV du fichier TOPO.


## Limitations

**Aucune garantie n'est apportée sur le résultat fourni.**

Il manque dans la sortie (infos non présentes dans TOPO) :
- le champ 'identifiant majic'
- le champ 'indicateur lieu dit non bati'
- les informations de population
- pas encore de support des dom-tom (corse ok)

## Utilisation

### prérequis

Un système d'exploitation permettant d'utiliser un shell, et python.


### Installation

Cloner ce projet : `git clone https://github.com/landryb/topo2fantoir.git`

Il n'y a pas de modules particuliers à installer.


### Téléchargement du fichier TOPO

Télécharger le fichier TOPO depuis [cette page](https://www.data.gouv.fr/fr/datasets/fichier-des-entites-topographiques-topo-dgfip-1/).

Ou utiliser cette commande : `curl -o topo-fichier-des-entites-topographiques.csv https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/topo-fichier-des-entites-topographiques/exports/csv`


### Création d'un fichier TOPO départemental

Pour alléger les traitements, on va extraire les données d'un seul département
de ce fichier national.

Pour cela il faut connaître le code administratif de la région. Se reporter au
tableau plus bas.

Exemple pour le département du Cantal (15) dans la région Auvergne-Rhône-Alpes
(84) :

```
$grep  ^991008415 topo-fichier-des-entites-topographiques.csv | sort > topo_15.csv
```

### Transformation du fichier TOPO en un fichier FANTOIR

Il faut passer le nom d'un fichier contenant des enregistrements du fichier
TOPO. Exemple :

```
$python3 convdep.py -i topo_15.csv > FANR_15.txt
```

Cela produira un fichier `FANR_15.txt dans le répertoire courant.

Pour les systèmes ne gérant pas correctement les redirections, il y'a également
une option `-o` pour écrire directement le résultat dans un fichier.

Ne pas oublier de comparer le résultat avec un fichier FANTOIR de l'année
précédente trié, pour retrouver plus facilement les nouvelles lignes. Ne pas
hésiter à comparer commune par commune.


## Table des régions

| REG | LIBELLE                      |
|-----|------------------------------|
| 1   | Guadeloupe                   |
| 2   | Martinique                   |
| 3   | Guyane                       |
| 4   | La Réunion                   |
| 6   | Mayotte                      |
| 11  | Île-de-France                |
| 24  | Centre-Val de Loire          |
| 27  | Bourgogne-Franche-Comté      |
| 28  | Normandie                    |
| 32  | Hauts-de-France              |
| 44  | Grand Est                    |
| 52  | Pays de la Loire             |
| 53  | Bretagne                     |
| 75  | Nouvelle-Aquitaine           |
| 76  | Occitanie                    |
| 84  | Auvergne-Rhône-Alpes         |
| 93  | Provence-Alpes-Côte d'Azur   |
| 94  | Corse                        |

