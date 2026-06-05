#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nom du fichier : enhance.py
Description : Donne du relief a des fichiers MIDI au jeu trop mecanique.
             Deux traitements complementaires, activables separement :
               - pedale : ajoute automatiquement la pedale forte (CC 64),
                 enfoncee a chaque temps et relachee juste avant le suivant ;
               - humanisation : fait varier velocites, departs de notes et
                 ajoute une legere derive de tempo (portage de l'algorithme
                 de vincerubinetti/midi-humanizer).
             Les hauteurs ne sont jamais modifiees.
Auteur : O. Booklage
Date : Juin 2026
Licence : CC BY-SA 4.0

Usage :
    python enhance.py "fichier.mid"             # pedale + humanisation
    python enhance.py "DOSSIER" --pedal         # pedale seule
    python enhance.py "fichier.mid" --humanize  # humanisation seule
Le resultat est ecrit a cote de la source, avec un suffixe.
"""

import os
import sys
import glob
import math
import random

from mido import MidiFile, MidiTrack, Message, MetaMessage


# --- Parametres d'humanisation ---
VELOCITE_ALEA = 18       # amplitude aleatoire de la velocite (unites MIDI)
VELOCITE_DECALAGE = -8   # decalage fixe (une velocite de 120 est trop forte)
TIMING_ALEA = 10         # amplitude aleatoire des departs de notes (tics)
DERIVE_AMPLITUDE = 8     # amplitude de la derive de tempo (tics)
DERIVE_PAS = 512         # espacement des points de derive (tics)
GRAINE = "midi"          # graine globale : meme entree -> meme sortie

# --- Parametres de pedale ---
PEDALE_UNITE_TEMPS = 1   # nombre de temps couverts par un coup de pedale
PEDALE_ECART = 32        # relache un 1/PEDALE_ECART de ronde avant le temps

# Suffixes selon les traitements appliques.
SUFFIXE_PEDALE = "-pedaled"
SUFFIXE_HUMANISE = "-humanized"
SUFFIXE_COMPLET = "-enhanced"


# ===============================================================
#  OUTILS COMMUNS
# ===============================================================

def alea(cle):
    """Renvoyer un nombre aleatoire deterministe dans [-1, 1].

    La meme cle produit toujours le meme nombre : les traitements
    sont donc reproductibles.

    Args:
        cle: Chaine servant de graine (par exemple "velocity3-12").

    Returns:
        Un flottant compris entre -1 et 1.
    """
    generateur = random.Random(cle)
    return generateur.uniform(-1, 1)


def borner(valeur, minimum, maximum):
    """Limiter une valeur a l'intervalle [minimum, maximum]."""
    return max(minimum, min(maximum, valeur))


def est_note_jouee(message):
    """Indiquer si le message demarre reellement une note."""
    return message.type == "note_on" and message.velocity > 0


def est_fin_de_note(message):
    """Indiquer si le message arrete une note (note_off ou note_on a 0)."""
    if message.type == "note_off":
        return True
    return message.type == "note_on" and message.velocity == 0


def vers_temps_absolu(piste):
    """Convertir une piste en liste [instant_absolu, message]."""
    evenements = []
    instant = 0
    for message in piste:
        instant += message.time
        evenements.append([instant, message])
    return evenements


def vers_piste(evenements):
    """Recomposer une piste a partir d'evenements en temps absolu.

    Les evenements sont retries par instant, les durees relatives
    (deltas) recalculees, et un end_of_track propre est ajoute.

    Args:
        evenements: Liste de [instant_absolu, message], le end_of_track
                    d'origine ayant ete retire au prealable.

    Returns:
        Une nouvelle piste MIDI.
    """
    evenements.sort(key=lambda evenement: evenement[0])
    piste = MidiTrack()
    instant_precedent = 0
    for instant, message in evenements:
        message.time = instant - instant_precedent
        instant_precedent = instant
        piste.append(message)
    piste.append(MetaMessage("end_of_track", time=0))
    return piste


def sans_fin_de_piste(evenements):
    """Retirer le message end_of_track de la liste d'evenements."""
    return [
        evenement
        for evenement in evenements
        if not (evenement[1].is_meta and evenement[1].type == "end_of_track")
    ]


# ===============================================================
#  PEDALE
# ===============================================================

def pedaliser_piste(piste, ticks_par_temps):
    """Ajouter une pedale forte rythmee a une piste contenant des notes.

    La pedale est enfoncee au debut, puis relachee juste avant chaque
    temps et reenfoncee sur le temps. Toute pedale existante est
    remplacee. Une piste sans note est renvoyee telle quelle.

    Args:
        piste: La piste MIDI d'origine.
        ticks_par_temps: Nombre de tics pour un temps (noire).

    Returns:
        Une nouvelle piste avec la pedale, ou la piste d'origine.
    """
    evenements = vers_temps_absolu(piste)
    notes_jouees = [(t, m) for t, m in evenements if est_note_jouee(m)]
    if not notes_jouees:
        return piste

    canal = notes_jouees[0][1].channel
    debut = notes_jouees[0][0]
    fin = max(t for t, m in evenements if est_fin_de_note(m))
    unite = max(1, ticks_par_temps * PEDALE_UNITE_TEMPS)
    ecart = max(1, (ticks_par_temps * 4) // PEDALE_ECART)

    def pedale(instant, valeur):
        message = Message(
            "control_change", control=64, value=valeur, channel=canal, time=0
        )
        return [instant, message]

    nouvelle_pedale = [pedale(debut, 127)]
    instant = debut + unite
    while instant < fin:
        nouvelle_pedale.append(pedale(instant - ecart, 0))
        nouvelle_pedale.append(pedale(instant, 127))
        instant += unite
    nouvelle_pedale.append(pedale(fin, 0))

    # Repartir des evenements en retirant l'ancienne pedale (CC 64).
    base = [
        evenement
        for evenement in sans_fin_de_piste(evenements)
        if not (
            evenement[1].type == "control_change" and evenement[1].control == 64
        )
    ]
    return vers_piste(base + nouvelle_pedale)


# ===============================================================
#  HUMANISATION
# ===============================================================

def construire_derive(duree_tics):
    """Construire la courbe de derive de tempo (instant -> decalage en tics).

    On tire un point aleatoire tous les DERIVE_PAS tics, puis on
    interpole entre ces points avec un lissage en sinus.

    Args:
        duree_tics: Duree totale de la piste, en tics.

    Returns:
        Une fonction qui, pour un instant en tics, renvoie un decalage.
    """
    pas = max(1, DERIVE_PAS)
    nombre_points = duree_tics // pas + 2
    points = [alea("derive" + str(i) + GRAINE) for i in range(nombre_points)]

    def derive(instant):
        position = instant / pas
        indice = int(position)
        fraction = position - indice
        lissage = 0.5 - math.cos(math.pi * fraction) / 2
        valeur = points[indice] + (points[indice + 1] - points[indice]) * lissage
        return valeur * DERIVE_AMPLITUDE

    return derive


def humaniser_piste(piste, index_piste, derive):
    """Humaniser une piste : velocites variees et departs decales.

    Le decalage de depart d'une note est applique a la fois a son
    note_on et a son note_off, ce qui preserve la duree des notes.

    Args:
        piste: La piste MIDI d'origine.
        index_piste: Numero de la piste (sert de graine).
        derive: Fonction de derive de tempo (voir construire_derive).

    Returns:
        Une nouvelle piste humanisee.
    """
    evenements = sans_fin_de_piste(vers_temps_absolu(piste))
    decalages_en_attente = {}
    index_note = 0
    for evenement in evenements:
        instant, message = evenement
        if est_note_jouee(message):
            decalage = alea("start" + str(index_piste) + str(index_note) + GRAINE)
            decalage = int(round(decalage * TIMING_ALEA + derive(instant)))
            nouvelle_velocite = (
                message.velocity
                + alea("velocity" + str(index_piste) + str(index_note) + GRAINE)
                * VELOCITE_ALEA
                + VELOCITE_DECALAGE
            )
            message.velocity = borner(int(round(nouvelle_velocite)), 1, 127)
            evenement[0] = max(0, instant + decalage)
            cle = (message.channel, message.note)
            decalages_en_attente.setdefault(cle, []).append(decalage)
            index_note += 1
        elif est_fin_de_note(message):
            cle = (message.channel, message.note)
            if decalages_en_attente.get(cle):
                decalage = decalages_en_attente[cle].pop(0)
                evenement[0] = max(0, instant + decalage)
    return vers_piste(evenements)


# ===============================================================
#  TRAITEMENT D'UN FICHIER
# ===============================================================

def suffixe(faire_pedale, faire_humanise):
    """Choisir le suffixe de nom selon les traitements appliques."""
    if faire_pedale and faire_humanise:
        return SUFFIXE_COMPLET
    if faire_pedale:
        return SUFFIXE_PEDALE
    return SUFFIXE_HUMANISE


def traiter_fichier(chemin, faire_pedale, faire_humanise):
    """Appliquer les traitements demandes a un fichier et l'enregistrer.

    Args:
        chemin: Chemin du fichier .mid d'entree.
        faire_pedale: Ajouter la pedale forte.
        faire_humanise: Appliquer l'humanisation.

    Returns:
        Le chemin du fichier ecrit.
    """
    midi = MidiFile(chemin)
    duree_tics = max(sum(m.time for m in piste) for piste in midi.tracks)
    derive = construire_derive(duree_tics)

    resultat = MidiFile(ticks_per_beat=midi.ticks_per_beat, type=midi.type)
    for index_piste, piste in enumerate(midi.tracks):
        if faire_pedale:
            piste = pedaliser_piste(piste, midi.ticks_per_beat)
        if faire_humanise:
            piste = humaniser_piste(piste, index_piste, derive)
        resultat.tracks.append(piste)

    base, extension = os.path.splitext(chemin)
    chemin_sortie = base + suffixe(faire_pedale, faire_humanise) + extension
    resultat.save(chemin_sortie)
    return chemin_sortie


def lister_fichiers(chemin):
    """Lister les fichiers a traiter (un seul ou tout un dossier).

    Les fichiers deja traites (suffixes connus) sont ignores.

    Args:
        chemin: Un fichier .mid ou un dossier.

    Returns:
        La liste triee des chemins a traiter.
    """
    if os.path.isfile(chemin):
        return [chemin]
    motif = os.path.join(chemin, "**", "*.mid")
    suffixes = (SUFFIXE_PEDALE, SUFFIXE_HUMANISE, SUFFIXE_COMPLET)
    fichiers = glob.glob(motif, recursive=True)
    return sorted(
        f for f in fichiers if not any(s in f for s in suffixes)
    )


def main():
    """Lire les arguments et traiter le fichier ou le dossier indique."""
    arguments = sys.argv[1:]
    options = [a for a in arguments if a.startswith("--")]
    chemins = [a for a in arguments if not a.startswith("--")]

    if not chemins:
        print('Usage : python enhance.py "fichier.mid" [--pedal] [--humanize]')
        return

    # Sans option : on applique les deux traitements.
    if not options:
        faire_pedale = True
        faire_humanise = True
    else:
        faire_pedale = "--pedal" in options
        faire_humanise = "--humanize" in options

    fichiers = lister_fichiers(chemins[0])
    total = len(fichiers)
    print(f"Traitement de {total} fichier(s)")
    for index, chemin in enumerate(fichiers, start=1):
        sortie = traiter_fichier(chemin, faire_pedale, faire_humanise)
        print(f"{index}/{total} {os.path.basename(sortie)}")
    print("** Terminé")


if __name__ == "__main__":
    main()
