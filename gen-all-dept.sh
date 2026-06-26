#!/bin/sh
set -e
# ne prend pas encore en compte les DOMTOM (97x)
for dpt in $(awk -F \; '/^99100;..;..;;;12/ {print $3}' topo-fichier-des-entites-topographiques.csv | sort -u) ; do
	echo $dpt
	if ! [ -f TOPO_${dpt}.csv ] ; then
		echo 'code_pays;code_region;code_dep;code_commune;code_voie;code_type_topo;nature_de_voie;libelle;type_commune_actuel_r_ou_n;type_commune_fip_r_ou_nfip;rur_actuel;rur_fip;caractere_voie;annulation;date_annulation;date_creation_de_article;type_voie;mot_classant;date_derniere_transition' > TOPO_${dpt}.csv
		egrep "^99100;..;${dpt};" topo-fichier-des-entites-topographiques.csv > TOPO_${dpt}_unsorted.csv
		# print dept header
		egrep "^99100;..;${dpt};;;12;" TOPO_${dpt}_unsorted.csv >> TOPO_${dpt}.csv
		for com in $(awk -F \; '/^99100;..;..;...;;13/ {print $4}' TOPO_${dpt}_unsorted.csv | sort -nu) ; do
			# print comm header
			egrep "^99100;..;${dpt};${com};;13;" TOPO_${dpt}_unsorted.csv >> TOPO_${dpt}.csv
			# print remaining lines, sorted by voie
			egrep "^99100;..;${dpt};${com};....;14;" TOPO_${dpt}_unsorted.csv | sort >> TOPO_${dpt}.csv
		done
		# for comparison with 2025 with code_topo
		sed -e 's/^.....;\(..\);\(..\);\(...\);\(....\);/99100\1\2\3\4/' TOPO_${dpt}.csv > TOPO_${dpt}_ctopo.csv
	fi
	[ -f FANR_${dpt}.txt ] || python3 convdep.py -i TOPO_${dpt}.csv > FANR_${dpt}.txt 2> FANR_${dpt}.log
	wc -l TOPO_${dpt}.csv FANR_${dpt}.txt
	gzip TOPO_${dpt}.csv
	gzip FANR_${dpt}.txt
done
