#!/usr/bin/env python3
'''
NAME
   word_freq - Calculates the word frequency in a text

SYNOPSIS
   word_freq [options] input_files
   options: 
        -m 20 : Shows the 20th most frequent words
        -n : Order alfabetically
        -o : File write
   
Description'''

from jjcli import * 
from collections import Counter
import sys
import re

cl=clfilter("o:nm", doc=__doc__)

def tokaniza(texto):
    palavras = re.findall(r'\w+(?:\-\w+)?|[.,?!;:—]+', texto)
    return palavras

def imprime(counter):
    for palavra, n_ocorr in counter:
        print(f"{palavra} --> {n_ocorr}")

def treat(counter: Counter) -> Counter:
    regex = re.compile(f"[A-ZÀ-Ÿ]")
    remove = []
    
    for palavra, n_ocorr in counter.items():
        if regex.search(palavra) and palavra.lower() in counter.keys():
            counter[palavra.lower()] += n_ocorr
            remove.append(palavra)

    for r in remove:
        del counter[r]
    
    return counter

def file(counter : Counter) -> None:
    f = open("output.txt","w")
    for palavra, n_ocorr in counter:
        f.write(f"{palavra} --> {n_ocorr}\n")
    f.close()

        
for txt in cl.text(): 
    lista_palavras = tokaniza(txt)
    ocorr = Counter(lista_palavras)
    ocorr = treat(ocorr)
    if "-o" in cl.opt:
        file(sorted(ocorr.items()))
    if "-m" in cl.opt:
        imprime(ocorr.most_common(int(cl.opt.get("-m"))))
    if "-n" in cl.opt:
        imprime(sorted(ocorr.items()))
    else:
        imprime(ocorr.items())

