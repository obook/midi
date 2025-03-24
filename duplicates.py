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
        os.path.join(path, "**", "*.mid"),
        recursive=True,
    )
):

    files.append([file, md5(file)])

for item in files:
    file, md5 = item
    print(file, md5)
