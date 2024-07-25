#!/bin/sh
set -e
# ne prend pas encore en compte les DOMTOM (97x)
for dpt in $(awk -F \; '/^99100....       12;/ { print substr($1,8,2) }' topo-fichier-des-entites-topographiques.csv | sort -u) ; do
	echo $dpt
	[ -f TOPO_${dpt}.csv ] || (echo 'code topo;libelle;type commune actuel (R ou N);type commune FIP (RouNFIP);RUR actuel;RUR FIP;caractere voie;annulation;date annulation;date creation de article;type voie;mot classant;date derniere transition' > TOPO_${dpt}.csv && egrep "^99100..${dpt}" topo-fichier-des-entites-topographiques.csv | sort >> TOPO_${dpt}.csv)
	[ -f FANR_${dpt}.txt ] || python3 convdep.py -i TOPO_${dpt}.csv > FANR_${dpt}.txt 2> FANR_${dpt}.log
	wc -l TOPO_${dpt}.csv FANR_${dpt}.txt
	gzip TOPO_${dpt}.csv
	gzip FANR_${dpt}.txt
done
