#!/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

import csv
import argparse
import codecs
import sys
import logging
from locale import atoi
from cle import compute_cle, insee2dir

natv = list()
with open("natv.txt", "r") as natvf:
    natv = natvf.read().split("\n")
# TOPO contient ces valeurs aussi pour nationale/departementale/voie ?
natv.extend(("N   ", "D   ", "V   "))

outfd = sys.stdout

logging.basicConfig(level=logging.INFO, format="%(message)s")


# https://python.jpvweb.com/python/mesrecettespython/doku.php?id=calcul_de_dates#donne_le_numero_du_jour_de_l_annee
def numjouran(j, m, a):
    """Donne le numéro du jour dans l'année de la date d=[j,m,a] (1er janvier = 1, ...)"""
    if (a % 4 == 0 and a % 100 != 0) or a % 400 == 0:  # bissextile?
        return (0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335, 366)[m - 1] + j
    else:
        return (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365)[m - 1] + j


def print_voie(row, curtypecomm, currurcomm):
    # 991008415001000114;GR  GRANDE RUE ABBE DE PRADT;;;;;0;;00000000;19870101;1;PRADT;20050524
    # 1500010001YGR  GRANDE RUE ABBE DE PRADT   N  3  0          00000000000000 00000001987001               002621   PRADT
    code = row["code topo"]
    date = row["date creation de article"]
    natvoie = "    "
    if row["libelle"][0:4] in natv:
        natvoie = row["libelle"][0:4]
        libelle = row["libelle"][4:].ljust(27)
    else:
        libelle = row["libelle"].ljust(27)
    # pas d'info sur le fait qu'un lieu dit soit habité ou pas dans TOPO -> 1 par défaut
    carlieudit = "1"
    if row["type voie"] == "4":
        carlieudit = " "
    #    print("{} -> '{}' + '{}'".format(row["libelle"][0:4], natvoie, libelle))
    # conversion de YYYYMMDD en YYYYQQQ
    sdate = "{}{:03d}".format(
        date[0:4], numjouran(atoi(date[6:]), atoi(date[4:6]), atoi(date[0:4]))
    )
    args = {
        "dept": code[7:9],
        "dir": insee2dir.get(code[7:12],"0"),
        "inseerivo": code[9:16],
        "clerivo": compute_cle(code),
        "natvoie": natvoie,
        "libelle": libelle,
        "curtypecomm": curtypecomm,
        "currurcomm": currurcomm,
        "caracterevoie": row["caractere voie"],
        "nopopinfo": "".ljust(14, "0"),
        "datecreation": sdate.rjust(14, "0"),
        "nocodemajic": "".ljust(20),
        "typevoie": row["type voie"],
        "caracterelieudit": carlieudit,
        "motclassant": row["mot classant"],
    }
    print(
        "{dept}{dir}{inseerivo}{clerivo}{natvoie}{libelle}{curtypecomm}  {currurcomm}  {caracterevoie}          {nopopinfo} {datecreation}{nocodemajic}{typevoie}{caracterelieudit}  {motclassant}".format(
            **args
        ),
        file=outfd,
    )


def print_commune(row, curtypecomm, currurcomm):
    # 991008415001    13;ALLANCHE;N;N;3;3;;;00000000;18750101;;;00000000
    # 150001    VALLANCHE                       N  3      000128600000000000000 00000001987001
    code = row["code topo"]
    date = row["date creation de article"]
    sdate = "{}{:03d}".format(
        date[0:4], numjouran(atoi(date[6:]), atoi(date[4:6]), atoi(date[0:4]))
    )
    # some kind of default date ?
    if date == "18750101":
        sdate = "1987001"
    args = {
        "dept": code[7:9],
        "dir": insee2dir.get(code[7:12],"0"),
        "inseerivo": code[9:16],
        "clerivo": compute_cle(code),
        "libelle": row["libelle"].ljust(31),
        "curtypecomm": curtypecomm,
        "currurcomm": currurcomm,
        "nopopinfo": "      " + "".ljust(21, "0"),
        "datecreation": sdate.rjust(14, "0"),
    }
    logging.info(f"commune {code[7:12]} (dir {args['dir']}) ({row['libelle']})")
    print(
        "{dept}{dir}{inseerivo}{clerivo}{libelle}{curtypecomm}  {currurcomm}{nopopinfo} {datecreation}".format(
            **args
        ),
        file=outfd,
    )


def print_dep(row):
    # XX no support for non-0 direction
    # 991008415       12;CANTAL;;;;;;;00000000;17900304;;;00000000
    # 150        CANTAL                                          00000000000000 00000000000000
    code = row["code topo"]
    date = row["date creation de article"]
    sdate = "{}{:03d}".format(
        date[0:4], numjouran(atoi(date[6:]), atoi(date[4:6]), atoi(date[0:4]))
    )
    args = {
        "dept": code[7:9],
        "libelle": row["libelle"].ljust(48),
        "zero": "".ljust(14, "0"),
        "datecreation": sdate.rjust(14, "0"),
    }
    print("{dept}0        {libelle}{zero} {datecreation}".format(**args), file=outfd)


parser = argparse.ArgumentParser(
    description="""

    Ce script permet de créer un fichier compatible FANTOIR à partir des données TOPO.

    La sortie par défaut est sur la console, avec les messages de logging sur stderr.

    Exemple : python3 convdep.py -i TOPO_15.csv > FANR_15.txt

    En option (pour les systèmes ne sachant pas gérer correctement les
    sorties), on peut aussi écrire le résultat dans un fichier avec -o

    Exemple : python3 convdep.py -i TOPO_15.csv -o FANR_15.txt

    """,
    formatter_class=argparse.RawTextHelpFormatter,
)

parser.add_argument("-i", "--infile", help="le fichier CSV a traiter", required=True)
parser.add_argument("-o", "--outfile", help="le nom du fichier de sortie")

args = parser.parse_args()
if args.outfile:
    try:
        outfd = codecs.open(args.outfile, "w", encoding="utf-8")
    except FileNotFoundError:
        print(f"impossible d'ouvrir {args.outfile} en écriture")
        sys.exit(1)

try:
    csvfile = open(args.infile, newline="")
except FileNotFoundError:
    print(f"impossible d'ouvrir {args.infile} en lecture")
    sys.exit(1)

with csvfile:
    reader = csv.DictReader(
        csvfile,
        delimiter=";",
        fieldnames=(
            "code topo",
            "libelle",
            "type commune actuel (R ou N)",
            "type commune FIP (RouNFIP)",
            "RUR actuel",
            "RUR FIP",
            "caractere voie",
            "annulation",
            "date annulation",
            "date creation de article",
            "type voie",
            "mot classant",
            "date derniere transition",
        ),
    )
    curtypecomm = None
    currurcomm = None
    curcomm = None
    for row in reader:
        type_enr = row["code topo"][16:18]
        code_insee = row["code topo"][8:13]
        if type_enr == "12":
            # departement
            print_dep(row)
        elif type_enr == "13":
            # commune
            curcomm = code_insee
            curtypecomm = row["type commune actuel (R ou N)"]
            currurcomm = row["RUR actuel"]
            if curtypecomm == "R" and currurcomm == "":
                currurcomm = " "
            print_commune(row, curtypecomm, currurcomm)
        elif type_enr == "14":
            # voie
            print_voie(row, curtypecomm, currurcomm)
