#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 13:15:46 2025

@author: obooklage
"""
import os
import glob
import hashlib
from pathlib import Path, PurePath


def md5(fname):
    with open(fname, "rb") as f:
        digest = hashlib.file_digest(f, "md5")
    return digest.hexdigest()


path = "."
files = []

for file in sorted(
    glob.glob(
        os.path.join(path, "**", "*.mid"), recursive=True)
   ):
    files.append([file, md5(file)])

with open("duplicate.txt", "w") as f:
    counter = 0
    for index1 in range(len(files)-1):
        for index2 in range(index1, len(files)):
            if files[index1][1] == files[index2][1] and files[index1][0] != files[index2][0]:
                counter += 1
                s = f"Duplicate #{counter} {files[index1][0]} ~ {files[index2][0]}\n"
                print(s)
                f.write(s)
                '''
                BOB MACE :
                renomer files[index1][0] en files[index2][0]
                ./MACE BOB/WORLDNED.mid
                ./PIANO BAR/What the World Needs Now.mid
                
                on récupère What the World Needs Now.mid
                '''
                # os.remove(files[index2][0])
                # os.remove(files[index2][0])
                # path = pathlib.PurePath(file)
                # p = Path(files[index2][0])
                # print(PurePath(files[index2][0]))
                
# Ca déplace ? OUI en racine !
# os.rename("./MACE BOB/ALLTHING.mid", os.path.join("./MACE BOB","All Things You Are.mid"))
