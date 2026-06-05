#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nom du fichier : score.py
Description : Génère une partition PDF pour chaque fichier MIDI de la
             collection, en parcourant récursivement les sous-dossiers.
             Les fichiers qui possèdent déjà un PDF sont ignorés.
Auteur : O. Booklage
Date : Juin 2026
Licence : CC BY-SA 4.0

Prérequis : MuseScore 3
    $ sudo apt install musescore3
"""

import os
import glob
from pathlib import Path
from datetime import datetime
from subprocess import call, DEVNULL


# Commande MuseScore 3 utilisée pour convertir un MIDI en PDF.
COMMANDE_MUSESCORE = "mscore3"

# Dossier racine analysé : celui qui contient ce script.
DOSSIER_RACINE = os.path.dirname(os.path.abspath(__file__))


def chemin_pdf(fichier_midi):
    """Construire le chemin du PDF associe a un fichier MIDI.

    Le PDF porte le meme nom que le fichier MIDI et se trouve dans
    le meme dossier (seule l'extension change).

    Args:
        fichier_midi: Chemin du fichier .mid.

    Returns:
        Le chemin du fichier .pdf correspondant.
    """
    dossier = os.path.dirname(fichier_midi)
    nom_sans_extension = Path(fichier_midi).stem
    return os.path.join(dossier, nom_sans_extension + ".pdf")


def generer_partition(fichier_midi):
    """Generer la partition PDF d'un fichier MIDI avec MuseScore 3.

    Si le PDF existe deja, la generation est ignoree.

    Args:
        fichier_midi: Chemin du fichier .mid a convertir.

    Returns:
        True si une partition a ete generee, False si elle existait
        deja ou si la conversion a echoue.
    """
    fichier_pdf = chemin_pdf(fichier_midi)
    if os.path.exists(fichier_pdf):
        return False

    # QT_QPA_PLATFORM=offscreen permet a MuseScore de s'executer
    # sans serveur graphique (utile en ligne de commande).
    environnement = dict(os.environ, QT_QPA_PLATFORM="offscreen")
    code_retour = call(
        [COMMANDE_MUSESCORE, fichier_midi, "-o", fichier_pdf],
        env=environnement,
        stdout=DEVNULL,
        stderr=DEVNULL,
    )

    if code_retour != 0:
        print(f"|!| Conversion impossible : {fichier_midi}")
        return False
    return True


def trouver_fichiers_midi(dossier_racine):
    """Lister tous les fichiers .mid sous un dossier, recursivement.

    Args:
        dossier_racine: Dossier de depart de la recherche.

    Returns:
        La liste triee des chemins des fichiers .mid trouves.
    """
    motif = os.path.join(dossier_racine, "**", "*.mid")
    return sorted(glob.glob(motif, recursive=True))


def main():
    """Parcourir la collection et generer les partitions manquantes."""
    fichiers = trouver_fichiers_midi(DOSSIER_RACINE)
    total = len(fichiers)
    print(f"Génération des partitions pour {total} fichiers MIDI")

    nombre_generees = 0
    for index, fichier_midi in enumerate(fichiers, start=1):
        heure = datetime.now().strftime("%H:%M:%S")
        nom = os.path.relpath(fichier_midi, DOSSIER_RACINE)
        print(f"{index}/{total} {heure} {nom}")
        if generer_partition(fichier_midi):
            nombre_generees += 1

    print(f"** Terminé : {nombre_generees} partitions générées")


if __name__ == "__main__":
    main()
