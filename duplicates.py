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

with open("duplicate.txt", "w") as f:
    counter = 0
    for index1 in range(len(files)):
        for index2 in range(len(files)):
            if files[index1][1] == files[index2][1] and files[index1][0] != files[index2][0]:
                counter += 1
                s = f"#{counter} {files[index1][0]} ~ {files[index2][0]}\n"
                print(s)
                f.write(s)
                # os.remove(files[index2][0])
