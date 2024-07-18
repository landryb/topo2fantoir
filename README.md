# topo2fantoir

Vous utilisez un outil qui a besoin d'un fichier au format
[FANTOIR](https://fr.wikipedia.org/wiki/FANTOIR), et ce dernier n'est plus
produit depuis juillet 2023 / a été remplacé par le fichier
[TOPO](https://www.data.gouv.fr/fr/datasets/fichier-des-entites-topographiques-topo-dgfip-1/).
Mais votre outil n'a pas encore été mis à jour pour supporter ce nouveau
fichier.. (ex [plugin qgis cadastre](https://github.com/3liz/QgisCadastrePlugin/issues/345)).

ce bout de python essaie de 'recréer' un fichier départemental FANTOIR depuis
l'export CSV du fichier TOPO.

attention, il manque dans la sortie (infos non présentes dans TOPO):
- le champ 'identifiant majic'
- le champ 'indicateur lieu dit non bati'
- les informations de population

en entrée, il faut les données d'un département extraites du CSV france entière
de 580Mo, triées sur le premier champ, exemple pour le cantal (15):

```
$grep  ^991008415 topo-fichier-des-entites-topographiques.csv | sort > topo15.csv
$python3 convdep.py > gen15.txt
```

et comparer le résultat avec un fichier fantoir de l'année précédente trié,
pour retrouver plus facilement les nouvelles lignes - ne pas hesiter a comparer
commune par commune.

# DISCLAIMER

aucune garantie n'est apportée sur le résultat fourni.
