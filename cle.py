#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

from locale import atoi
salph = "ABCDEFGHJKLMNPRSTUVWXYZ"
# without I. O and Q
alph = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"
#full
#alph = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def compute_cle(code):
#    print("input={}".format(code))
    if code[7:9] == '2A':
        dpt = 3
    elif code[7:9] == '2B':
        dpt = 4
    else:
        dpt = atoi(code[7:9])
    ins = atoi(code[9:12])
    comm = dpt * 10000 + ins
    riv = code[12:16]
    if riv == '    ':
        ordre = comm % 23
    else:
        numv = atoi(riv[1:4])
        if riv[0] == 'I':
            code = alph.index('A')
        elif riv[0] == 'O':
            code = alph.index('B')
        elif riv[0] == 'Q':
            code = alph.index('C')
        else:
            code = alph.index(riv[0])
#        print('numv={}, riv[0] = {} -> index = {}'.format(numv, riv[0], code))
        ordre = ((19 * comm) + (11 * code) + numv) % 23
#    print("dpt={}, ins={}, commune={}, code riv='{}' -> ordre={}".format(dpt,ins,comm, riv, ordre))
    #print("salph[0]={}".format(salph[0]))
    return salph[ordre]

tests=(
{ 'code_topo': '991008415258    ', 'code_fantoir': '150258    Z' }, #dept 15: commune de VIC-SUR-CERE
{ 'code_topo': '9910084014570690', 'code_fantoir': '0104570690K' }, #dept 01: RTE DE NAMARY
{ 'code_topo': '991008415001A030', 'code_fantoir': '150001A030Z' }, #dept 15: CITEFROMENTS
{ 'code_topo': '99100942A092B180', 'code_fantoir': '2A0092B180T' }, #dept 2A: LAMAGHIONE
{ 'code_topo': '99100942A142B221', 'code_fantoir': '2A0142B221V' }, #dept 2A: FILAGHIONE
{ 'code_topo': '99100942B002    ', 'code_fantoir': '2B0002    F' }, #dept 2B: commune d'AGHIONE
{ 'code_topo': '99100942B002B001', 'code_fantoir': '2B0002B001L' }, #dept 2B: AGHIONE
{ 'code_topo': '991002814061I975', 'code_fantoir': '140061I975P' }, #dept 14: LES FARCIERES
{ 'code_topo': '991005249331I874', 'code_fantoir': '490331I874W' }, #dept 49: GRANDE FROMENTRIE
{ 'code_topo': '991002850041I996', 'code_fantoir': '500041I996L' }, #dept 50: LA BISSONNERIE
{ 'code_topo': '991002850041J998', 'code_fantoir': '500041J998J' }, #dept 50: LA RIGNOLETTERIE VAUVILLE
{ 'code_topo': '991002814061J030', 'code_fantoir': '140061J030M' }, #dept 14: LA GRANDE BINOTIERE
{ 'code_topo': '991002850041K421', 'code_fantoir': '500041K421U' }, #dept 50: LE SEMAPHORE DE JARDEHEU
{ 'code_topo': '991005249092L222', 'code_fantoir': '490092L222W' }, #dept 49: CHANTELEVENT
{ 'code_topo': '991005329024M008', 'code_fantoir': '290024M008L' }, #dept 29: KERGALET VRAZ
{ 'code_topo': '991005356026N001', 'code_fantoir': '560026N001U' }, #dept 56: BAS DE KERFAVEN
{ 'code_topo': '991005322185O090', 'code_fantoir': '220185O090D' }, #dept 22: LES PALMIERS
{ 'code_topo': '991007540185O068', 'code_fantoir': '400185O068W' }, #dept 40: LAHITTE
{ 'code_topo': '991002445252O912', 'code_fantoir': '450252O912F' }, #dept 45: PCE ST EXUPERY
{ 'code_topo': '991005285194P759', 'code_fantoir': '850194P759E' }, #dept 85: LE DEGAST
{ 'code_topo': '991005322093P710', 'code_fantoir': '220093P710W' }, #dept 22: LES BERGEONS  MESLIN
{ 'code_topo': '991005322093Q032', 'code_fantoir': '220093Q032C' }, #dept 22: CLOTURE JARNOT
{ 'code_topo': '991005285194Q844', 'code_fantoir': '850194Q844R' }, #dept 85: PARC D ACTILONNE
{ 'code_topo': '991005285194Q843', 'code_fantoir': '850194Q843P' }, #dept 85: LA FONSSAUCE
{ 'code_topo': '991005285202R493', 'code_fantoir': '850202R493T' }, #dept 85: LES GROIES
{ 'code_topo': '991007519130S110', 'code_fantoir': '190130S110S' }, #dept 19: ROTONDES FONFREYDE
{ 'code_topo': '991003262126T349', 'code_fantoir': '620126T349R' }, #dept 62: L ESTRACELLE
{ 'code_topo': '991009313103V029', 'code_fantoir': '130103V029A' }, #dept 13: RES VERT BOCAGE
{ 'code_topo': '991009313001V110', 'code_fantoir': '130001V110G' }, #dept 13: CHATEAU DE LUYNES NORD
{ 'code_topo': '991002827467W109', 'code_fantoir': '270467W109X' }, #dept 27: LA SENTE MAILLERAIE
{ 'code_topo': '991008401053X022', 'code_fantoir': '010053X022Z' }, #dept 01: PKG DES BONS ENFANTS
{ 'code_topo': '991008401288X006', 'code_fantoir': '010288X006J' }, #dept 01: PKG DE L'ETRAZ
{ 'code_topo': '991008415014X004', 'code_fantoir': '150014X004D' }, #dept 15: CANAL DE PEYROLLES
# ces 2 voies avec Y comme première lettre du code rivoli ne se retrouvent plus avec le meme code rivoli dans TOPO -> changement de zone ?
#fantoir:    160102Y004ECITELE CLOS GIRARDIN
#topo: 991007516102102514;CITELE CLOS GIRARDIN
#fantoir:    110069Y046K    DE STE MARIE
#topo: 991007611069423814;CHE DE STE MARIE
)
if __name__ == '__main__':
    for t in tests:
        cle = compute_cle(t['code_topo'])
        if t['code_fantoir'][-1] != cle:
            print(f"{t['code_topo']} expects {t['code_fantoir'][-1]} returns {cle}")
        else:
            print(f"{t['code_topo']} key matches")
        #	assert compute_cle(t['code_topo']) == t['code_fantoir'][-1]
