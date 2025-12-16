#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 13:15:46 2025

@author: obooklage
"""
import os
import glob
import hashlib


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

# print(files)

with open("duplicate.txt", "w") as f:
    counter = 0
    for index1 in range(len(files)):
        for index2 in range(len(files)):

            file_1 = files[index1][0]
            md5_1 = files[index1][1]

            file_2 = files[index2][0]
            md5_2 = files[index2][1]

            if md5_1 == md5_2 and file_1 != file_2:
                counter += 1
                s = f"#{counter} {files[index1][0]} ~ {files[index2][0]}\n"
                print(s)
                f.write(s)
                # os.remove(files[index2][0]) # and pdf ?

            # Windows name collision (case-insensitive filesystem)
            if file_1 != file_2 and file_1.upper() == file_2.upper():
                s = f"Same md5 : [{files[index1][0]}] and [{files[index2][0]}]\n"
                print(s)
                # os.rename('a.txt', 'b.kml')
