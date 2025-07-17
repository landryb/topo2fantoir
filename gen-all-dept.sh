#!/bin/sh
set -e
# ne prend pas encore en compte les DOMTOM (97x)
for dpt in $(awk -F \; '/^99100....       12;/ { print substr($1,8,2) }' topo-fichier-des-entites-topographiques.csv | sort -u) ; do
	echo $dpt
	[ -f TOPO_${dpt}.csv ] || (echo 'code_topo;nature_de_voie;libelle;type_commune_actuel_r_ou_n;type_commune_fip_r_ou_nfip;rur_actuel;rur_fip;caractere_voie;annulation;date_annulation;date_creation_de_article;type_voie;mot_classant;date_derniere_transition' > TOPO_${dpt}.csv && egrep "^99100..${dpt}" topo-fichier-des-entites-topographiques.csv | sort >> TOPO_${dpt}.csv)
	[ -f FANR_${dpt}.txt ] || python3 convdep.py -i TOPO_${dpt}.csv > FANR_${dpt}.txt 2> FANR_${dpt}.log
	wc -l TOPO_${dpt}.csv FANR_${dpt}.txt
	gzip TOPO_${dpt}.csv
	gzip FANR_${dpt}.txt
done
