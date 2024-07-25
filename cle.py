#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 et

from locale import atoi
salph = "ABCDEFGHJKLMNPRSTUVWXYZ"
# without U and Z
alph = "0123456789ABCDEFGHIJKLMNOPQRSTVWXY"
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
        code = alph.index(riv[0])
#        print('numv={}, riv[0] = {} -> index = {}'.format(numv, riv[0], code))
        ordre = ((19 * comm) + (11 * code) + numv) % 23
#    print("dpt={}, ins={}, commune={}, code riv='{}' -> ordre={}".format(dpt,ins,comm, riv, ordre))
    #print("salph[0]={}".format(salph[0]))
    return salph[ordre]

tests=(
{ 'code_topo': '991005322185O090', 'code_fantoir': '220185O090D' }, #dept 22: LES PALMIERS
{ 'code_topo': '991008415258    ', 'code_fantoir': '150258    Z' }, #dept 15: commune de VIC-SUR-CERE
{ 'code_topo': '991008415001A030', 'code_fantoir': '150001A030Z' }, #dept 15: CITEFROMENTS
{ 'code_topo': '99100942A092B180', 'code_fantoir': '2A0092B180T' }, #dept 2A: LAMAGHIONE
{ 'code_topo': '99100942A142B221', 'code_fantoir': '2A0142B221V' }, #dept 2A: FILAGHIONE
{ 'code_topo': '99100942B002    ', 'code_fantoir': '2B0002    F' }, #dept 2B: commune d'AGHIONE
{ 'code_topo': '99100942B002B001', 'code_fantoir': '2B0002B001L' }, #dept 2B: AGHIONE
{ 'code_topo': '991008401288X006', 'code_fantoir': '010288X006J' }, #dept 01: PKG DE L'ETRAZ
{ 'code_topo': '991002814061I975', 'code_fantoir': '140061I975P' }, #dept 14: LES FARCIERES
{ 'code_topo': '991002850041K421', 'code_fantoir': '500041K421U' }, #dept 50: LE SEMAPHORE DE JARDEHEU
{ 'code_topo': '991005329024M008', 'code_fantoir': '290024M008L' }, #dept 29: KERGALET VRAZ
{ 'code_topo': '991002850041J998', 'code_fantoir': '500041J998J' }, #dept 50: LA RIGNOLETTERIE VAUVILLE
)
if __name__ == '__main__':
    for t in tests:
        print(f"{t['code_topo']} expects {t['code_fantoir'][-1]} returns {compute_cle(t['code_topo'])}")
        #	assert compute_cle(t['code_topo']) == t['code_fantoir'][-1]
