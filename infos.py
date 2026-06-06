#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nom du fichier : infos.py
Description : Génère un fichier d'informations JSON à côté de chaque
             fichier MIDI de la collection (piece.mid -> piece.json).
             Chaque sidecar contient le titre, le compositeur, la durée,
             l'état humanisé, la pédale, le nombre de notes, le tempo et
             la signature rythmique.
             Les clés JSON sont en anglais ; le code reste en français.
Auteur : O. Booklage
Date : Juin 2026
Licence : CC BY-SA 4.0

Usage :
    python infos.py          # met à jour les sidecars (garde score_title)
    python infos.py --force  # réécrit tout, y compris score_title
"""

import os
import re
import sys
import json

from mido import MidiFile, tempo2bpm

# Réutilisation des règles communes déjà définies pour les partitions.
from score import nom_compositeur, titre_morceau, trouver_fichiers_midi


# Dossier racine analysé : celui qui contient ce script.
DOSSIER_RACINE = os.path.dirname(os.path.abspath(__file__))

# Fichier listant les morceaux humanisés (chemins entre accents graves).
FICHIER_HUMANISES = os.path.join(DOSSIER_RACINE, "HUMANIZED.md")


def chemin_sidecar(fichier_midi):
    """Construire le chemin du sidecar JSON associé à un fichier MIDI.

    Le JSON porte le même nom que le fichier MIDI, dans le même
    dossier (seule l'extension change).

    Args:
        fichier_midi: Chemin du fichier .mid.

    Returns:
        Le chemin du fichier .json correspondant.
    """
    base, _ = os.path.splitext(fichier_midi)
    return base + ".json"


def charger_fichiers_humanises():
    """Lire HUMANIZED.md et renvoyer l'ensemble des fichiers humanisés.

    Les chemins y sont écrits entre accents graves, par exemple
    `DOSSIER/morceau.mid`.

    Returns:
        Un ensemble de chemins relatifs (str) ; vide si le fichier est
        absent.
    """
    if not os.path.exists(FICHIER_HUMANISES):
        return set()
    with open(FICHIER_HUMANISES, encoding="utf-8") as fichier:
        contenu = fichier.read()
    # Capture tout ce qui est entre accents graves et finit par .mid
    return set(re.findall(r"`([^`]+\.mid)`", contenu))


def formater_duree(secondes):
    """Mettre en forme une durée au format minutes:secondes.

    Args:
        secondes: Durée en secondes.

    Returns:
        Une chaîne de la forme "m:ss" (par exemple "3:07").
    """
    minutes = int(secondes) // 60
    reste = int(secondes) % 60
    return f"{minutes}:{reste:02d}"


def analyser_midi(chemin):
    """Extraire les informations musicales d'un fichier MIDI.

    Parcourt le fichier une seule fois en temps réel (secondes) pour
    mesurer la durée jusqu'à la dernière note et compter les notes, les
    coups de pédale, le premier tempo et la première signature.

    Args:
        chemin: Chemin du fichier .mid.

    Returns:
        Un dictionnaire de mesures, ou None si la lecture échoue.
    """
    try:
        midi = MidiFile(chemin)
        temps_ecoule = 0.0
        temps_derniere_note = 0.0
        nombre_notes = 0
        evenements_pedale = 0
        tempo_bpm = None
        signature = None
        for message in midi:
            temps_ecoule += message.time
            if message.type == "note_on" and message.velocity > 0:
                nombre_notes += 1
                temps_derniere_note = temps_ecoule
            elif message.type == "control_change" and message.control == 64:
                evenements_pedale += 1
            elif message.type == "set_tempo" and tempo_bpm is None:
                tempo_bpm = round(tempo2bpm(message.tempo))
            elif message.type == "time_signature" and signature is None:
                signature = f"{message.numerator}/{message.denominator}"
    except Exception as erreur:
        print(f"|!| Lecture impossible : {chemin} ({erreur})")
        return None

    # Valeurs par défaut du standard MIDI si rien n'est précisé.
    if tempo_bpm is None:
        tempo_bpm = 120
    if signature is None:
        signature = "4/4"

    return {
        "duration_seconds": round(temps_derniere_note),
        "note_count": nombre_notes,
        "pedal_events": evenements_pedale,
        "tempo_bpm": tempo_bpm,
        "time_signature": signature,
    }


def construire_infos(fichier_midi, fichiers_humanises):
    """Construire le dictionnaire d'informations d'un fichier MIDI.

    Args:
        fichier_midi: Chemin du fichier .mid.
        fichiers_humanises: Ensemble des chemins relatifs humanisés.

    Returns:
        Le dictionnaire prêt à être écrit en JSON, ou None si le MIDI
        est illisible.
    """
    analyse = analyser_midi(fichier_midi)
    if analyse is None:
        return None

    # Les underscores des noms de fichiers deviennent des espaces pour
    # un titre lisible ; le chemin (path) garde le vrai nom de fichier.
    titre = titre_morceau(fichier_midi).replace("_", " ")
    relatif = os.path.relpath(fichier_midi, DOSSIER_RACINE)
    relatif = relatif.replace(os.sep, "/")

    # Le compositeur et l'interprète partent du même nom de dossier ;
    # performer pourra être affiné à la main par la suite.
    nom = nom_compositeur(fichier_midi)

    return {
        "title": titre,
        "score_title": titre,
        "path": relatif,
        "composer": nom,
        "performer": nom,
        "date": "",
        "duration": formater_duree(analyse["duration_seconds"]),
        "duration_seconds": analyse["duration_seconds"],
        "humanized": relatif in fichiers_humanises,
        "pedal": {
            "present": analyse["pedal_events"] > 0,
            "events": analyse["pedal_events"],
        },
        "note_count": analyse["note_count"],
        "tempo_bpm": analyse["tempo_bpm"],
        "time_signature": analyse["time_signature"],
    }


# Champs renseignés à la main et donc préservés lors des mises à jour.
CHAMPS_PRESERVES = ("score_title", "performer", "date")


def lire_sidecar_existant(chemin_json):
    """Charger un sidecar JSON existant, s'il est lisible.

    Args:
        chemin_json: Chemin du fichier .json.

    Returns:
        Le dictionnaire chargé, ou None si le fichier est absent ou
        illisible.
    """
    if not os.path.exists(chemin_json):
        return None
    try:
        with open(chemin_json, encoding="utf-8") as fichier:
            return json.load(fichier)
    except (ValueError, OSError):
        return None


def generer_infos(fichier_midi, fichiers_humanises, forcer=False):
    """Écrire (ou mettre à jour) le sidecar JSON d'un fichier MIDI.

    Sans forcer, un score_title déjà présent est conservé (édition
    manuelle). Avec forcer, tous les champs sont réécrits.

    Args:
        fichier_midi: Chemin du fichier .mid.
        fichiers_humanises: Ensemble des chemins relatifs humanisés.
        forcer: Réécrire aussi score_title.

    Returns:
        True si le sidecar a été écrit, False si le MIDI est illisible.
    """
    infos = construire_infos(fichier_midi, fichiers_humanises)
    if infos is None:
        return False

    fichier_json = chemin_sidecar(fichier_midi)
    if not forcer:
        ancien = lire_sidecar_existant(fichier_json)
        if ancien is not None:
            # Conserver les champs renseignés à la main.
            for cle in CHAMPS_PRESERVES:
                if cle in ancien:
                    infos[cle] = ancien[cle]

    with open(fichier_json, "w", encoding="utf-8") as fichier:
        json.dump(infos, fichier, ensure_ascii=False, indent=2)
        fichier.write("\n")
    return True


def main():
    """Générer les sidecars JSON de toute la collection."""
    forcer = "--force" in sys.argv[1:]

    fichiers_humanises = charger_fichiers_humanises()
    fichiers = trouver_fichiers_midi(DOSSIER_RACINE)
    total = len(fichiers)
    print(f"Génération des informations pour {total} fichiers MIDI")

    nombre_ecrits = 0
    for fichier_midi in fichiers:
        if generer_infos(fichier_midi, fichiers_humanises, forcer=forcer):
            nombre_ecrits += 1

    print(f"** Terminé : {nombre_ecrits} fichiers d'informations écrits")


if __name__ == "__main__":
    main()
