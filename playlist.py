#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nom du fichier : playlist.py
Description : Genere PLAYLIST.md, un classement par duree croissante
             de morceaux celebres et accessibles (debutant a moyen),
             selectionnes a la main dans la collection.
Auteur : O. Booklage
Date : Juin 2026
Licence : CC BY-SA 4.0
"""

import os

from mido import MidiFile


# Selection curee : uniquement des morceaux celebres, jouables par un
# interprete debutant a intermediaire. Un seul fichier par morceau
# (les doublons de la collection sont volontairement ecartes).
# Niveau : 1 = debutant, 2 = facile, 3 = intermediaire (moyen).
REPERTOIRE = [
    # --- Comptines et chants tres connus (debutant) ---
    ("ENFANTS CHILD/Au-Clair-de-la-Lune.mid", "Au clair de la lune", "Traditionnel", 1),
    ("ENFANTS CHILD/Frere_Jacques.mid", "Frère Jacques", "Traditionnel", 1),
    ("ENFANTS CHILD/Ah_vous_dirais_je_Maman.mid", "Ah vous dirai-je maman", "Traditionnel", 1),
    ("ENFANTS CHILD/Vive_le_vent.mid", "Vive le vent", "Traditionnel", 1),
    ("ENFANTS CHILD/Douce_Nuit.mid", "Douce nuit (Silent Night)", "F. Gruber", 1),
    ("ENFANTS CHILD/Mon_beau_sapin.mid", "Mon beau sapin", "Traditionnel", 1),
    ("ENFANTS CHILD/Sur_le_pont_d_Avignon.mid", "Sur le pont d'Avignon", "Traditionnel", 1),

    # --- Classiques accessibles (facile a intermediaire) ---
    ("SATIE ERIK/Gymnopedie No - simple.mid", "Gymnopédie n°1", "E. Satie", 2),
    ("SATIE ERIK/Gymnopedie No.3.mid", "Gymnopédie n°3", "E. Satie", 2),
    ("SATIE ERIK/Gnossiennes 1890 1 K.Oguri - Lent.mid", "Gnossienne n°1", "E. Satie", 3),
    ("SATIE ERIK/Gnossiennes 1890 2 K.Oguri - Etonnement.mid", "Gnossienne n°2", "E. Satie", 3),
    ("SATIE ERIK/Gnossiennes 1890 3 K.Oguri - Lent.mid", "Gnossienne n°3", "E. Satie", 3),
    ("CLEMENTI MUZIO/Sonatina Opus.36, No.1.mid", "Sonatine Op. 36 n°1", "M. Clementi", 2),
    ("BACH JOHANN SEBASTIAN/Jesu, Joy of Man’s Desiring, BWV 147.mid", "Jésus que ma joie demeure, BWV 147", "J.-S. Bach", 3),
    ("BACH JOHANN SEBASTIAN/Air On A G String (J S Bach).mid", "Air sur la corde de sol", "J.-S. Bach", 2),
    ("BACH JOHANN SEBASTIAN/Prelude and Fugue in C major BWV 846.mid", "Prélude en ut majeur, BWV 846", "J.-S. Bach", 3),
    ("CHOPIN FREDERIC/Prelude-in-C-Minor-Opus-28-Nr-20.mid", "Prélude Op. 28 n°20", "F. Chopin", 2),
    ("CHOPIN FREDERIC/Prelude Op.28 No.4 in e.mid", "Prélude Op. 28 n°4", "F. Chopin", 3),
    ("MOZART WOLFGANG AMADEUS/Piano Sonata No. 16 in C major, KV 545 _1_Allegro.mid", "Sonate facile K. 545, Allegro", "W. A. Mozart", 3),
    ("MOZART WOLFGANG AMADEUS/Piano Sonata No. 16 in C major, KV 545 _2_Andante.mid", "Sonate facile K. 545, Andante", "W. A. Mozart", 3),
    ("BEETHOVEN LUDWIG VAN/6101-2d_moonlight_sonata_27-2_1_2_(nc)smythe.mid", "Sonate Clair de lune, 1er mouvement", "L. van Beethoven", 3),
    ("MOZART WOLFGANG AMADEUS/Piano Sonata No. 11 in A major, KV 331_3_Alla turca-Allegretto.mid", "Marche turque (Rondo Alla Turca)", "W. A. Mozart", 3),
    ("CHOPIN FREDERIC/Nocturne Op. 9 No. 2 in E-flat Major.mid", "Nocturne Op. 9 n°2", "F. Chopin", 3),
    ("CHOPIN FREDERIC/Mazurka in B Minor, Op. 33 No. 4.mid", "Mazurka Op. 33 n°4", "F. Chopin", 3),
    ("CHOPIN FREDERIC/Etude Op. 25 No. 3 in F Major.mid", "Étude Op. 25 n°3", "F. Chopin", 4),
    ("GRIEG EDVARD/In the hall of the Mountain King.mid", "Dans l'antre du roi de la montagne", "E. Grieg", 3),
    ("DVORAK ANTONIN/Humoresque.mid", "Humoresque n°7", "A. Dvořák", 3),
    ("ALBÉNIZ ISAAC/Tango.mid", "Tango (España, Op. 165)", "I. Albéniz", 3),
    ("RAGTIME/Scott Joplin - Entertainer.mid", "The Entertainer", "S. Joplin", 3),

    # --- Films, chansons et standards celebres (arrangements accessibles) ---
    ("FILMS/My-Heart-Will-Go-On-(From-'Titanic')-piano.mid", "My Heart Will Go On (Titanic)", "J. Horner", 2),
    ("POP-FRANCE/Yann Tiersen - Comptine dun autre ete1.mid", "Comptine d'un autre été (Amélie Poulain)", "Y. Tiersen", 2),
    ("POP-FRANCE/Yann Tiersen - Valse Amélie Poulain-piano.mid", "La Valse d'Amélie", "Y. Tiersen", 3),
    ("POP-INTER/Ludovico Einaudi - Experience.mid", "Experience", "L. Einaudi", 3),
    ("POP-INTER/Alan_Walker_Faded.mid", "Faded", "Alan Walker", 2),
    ("POP-INTER/Gary Jules - Mad World.mid", "Mad World", "Gary Jules", 2),
    ("POP-INTER/Lewis Capaldi - Someone You Loved.mid", "Someone You Loved", "L. Capaldi", 2),
    ("POP-INTER/Sting - Shape Of My Heart.mid", "Shape of My Heart", "Sting", 3),
    ("POP-INTER/Bruno Mars - Talking to the moon.mid", "Talking to the Moon", "Bruno Mars", 2),
    ("POP-BEATLES/LetItBe.mid", "Let It Be", "The Beatles", 2),
    ("POP-BEATLES/Imagine.mid", "Imagine", "John Lennon", 2),
    ("POP-BEATLES/Hey Jude.mid", "Hey Jude", "The Beatles", 2),
    ("POP-BEATLES/Michelle.mid", "Michelle", "The Beatles", 3),
    ("ABBA/The_Winner_Takes_It_All.mid", "The Winner Takes It All", "ABBA", 3),
    ("ABBA/Chiquitita.mid", "Chiquitita", "ABBA", 3),
    ("ABBA/MammaMia.mid", "Mamma Mia", "ABBA", 3),
    ("QUEEN/We are the Champions.mid", "We Are the Champions", "Queen", 3),
    ("POP-70/Carpenters-Close_to_you.mid", "(They Long to Be) Close to You", "Carpenters", 2),
    ("POP-70/Carpenters-Yesterday-Once-More.mid", "Yesterday Once More", "Carpenters", 2),
    ("POP-70/Morris Albert - Feelings.mid", "Feelings", "Morris Albert", 2),
    ("PIANO BAR/Piano Man.mid", "Piano Man", "Billy Joel", 3),
    ("PIANO BAR/Killing Me Softly.mid", "Killing Me Softly", "R. Flack", 2),
    ("PIANO BAR/Wonderful World.mid", "What a Wonderful World", "L. Armstrong", 2),
    ("PIANO BAR/Stardust.mid", "Stardust", "H. Carmichael", 3),
]

# Etiquettes affichees pour chaque niveau de difficulte.
LIBELLES_NIVEAU = {
    1: "Débutant",
    2: "Facile",
    3: "Intermédiaire",
    4: "Avancé",
}

# Morceaux celebres et accessibles ABSENTS de la collection qu'il
# serait pertinent d'ajouter. Verifie : aucun de ces titres n'est
# present dans les fichiers .mid du depot.
# Format : (titre, compositeur, niveau).
MANQUANTS = [
    ("Lettre à Élise (Für Elise), WoO 59", "L. van Beethoven", 2),
    ("Hymne à la joie (thème)", "L. van Beethoven", 1),
    ("Canon en ré majeur", "J. Pachelbel", 3),
    ("Menuet en sol majeur, BWV Anh. 114", "J.-S. Bach", 1),
    ("Solfeggietto", "C. P. E. Bach", 3),
    ("Rêverie (Träumerei), Scènes d'enfants", "R. Schumann", 3),
    ("La fille aux cheveux de lin", "C. Debussy", 3),
    ("Rêverie", "C. Debussy", 3),
    ("Ave Maria", "F. Schubert", 3),
    ("Sérénade", "F. Schubert", 3),
    ("Moment musical n°3", "F. Schubert", 3),
    ("Romance sans paroles (Chant de printemps)", "F. Mendelssohn", 3),
    ("Au matin (Peer Gynt)", "E. Grieg", 2),
    ("Album pour la jeunesse (pièces faciles)", "P. I. Tchaïkovski", 1),
    ("Arabesque, Op. 100 n°2", "F. Burgmüller", 2),
    ("Rêve d'amour (Liebestraum n°3)", "F. Liszt", 3),
    ("Maple Leaf Rag", "S. Joplin", 3),
    ("Lacrimosa (Requiem)", "W. A. Mozart", 3),
    ("River Flows in You", "Yiruma", 3),
    ("Ballade pour Adeline", "R. Clayderman", 3),
    ("Hallelujah", "L. Cohen", 2),
    ("Someone Like You", "Adele", 2),
    ("All of Me", "J. Legend", 2),
    ("Perfect", "Ed Sheeran", 2),
    ("Clocks", "Coldplay", 3),
]


def calculer_duree(chemin):
    """Calculer la duree musicale d'un fichier MIDI en secondes.

    On mesure le temps ecoule jusqu'a la derniere note jouee, et non
    la duree brute du fichier : certains fichiers de la collection
    contiennent un long silence final (un evenement avec un delta de
    plusieurs centaines de milliers de tics) qui fausserait le tri.

    Args:
        chemin: Chemin du fichier .mid a analyser.

    Returns:
        La duree en secondes (float), ou None si la lecture echoue.
    """
    try:
        midi = MidiFile(chemin)
        temps_ecoule = 0.0
        temps_derniere_note = 0.0
        # En iterant sur le fichier, mido fournit message.time en
        # secondes (en tenant compte des changements de tempo).
        for message in midi:
            temps_ecoule += message.time
            if message.type in ("note_on", "note_off"):
                temps_derniere_note = temps_ecoule
        return temps_derniere_note
    except Exception as erreur:
        print(f"|!| Lecture impossible : {chemin} ({erreur})")
        return None


def formater_duree(secondes):
    """Mettre en forme une duree au format minutes:secondes.

    Args:
        secondes: Duree en secondes.

    Returns:
        Une chaine de la forme "m:ss" (par exemple "3:07").
    """
    minutes = int(secondes) // 60
    reste = int(secondes) % 60
    return f"{minutes}:{reste:02d}"


def construire_lignes():
    """Lire la duree de chaque morceau et trier par duree croissante.

    Returns:
        Une liste de tuples (duree_secondes, titre, compositeur,
        niveau, chemin), triee par duree croissante. Les fichiers
        absents ou illisibles sont ignores.
    """
    lignes = []
    for chemin, titre, compositeur, niveau in REPERTOIRE:
        if not os.path.exists(chemin):
            print(f"|!| Fichier introuvable : {chemin}")
            continue
        duree = calculer_duree(chemin)
        if duree is None:
            continue
        lignes.append((duree, titre, compositeur, niveau, chemin))

    lignes.sort(key=lambda ligne: ligne[0])
    return lignes


def ecrire_playlist(lignes):
    """Ecrire le fichier PLAYLIST.md a partir des morceaux tries.

    Args:
        lignes: Liste de tuples (duree, titre, compositeur, niveau,
                chemin) triee par duree croissante.
    """
    with open("PLAYLIST.md", "w", encoding="utf-8") as fichier:
        fichier.write("# Playlist - morceaux célèbres et accessibles\n\n")
        fichier.write(
            "Classement par durée croissante de morceaux célèbres, "
            "pour un interprète débutant à intermédiaire.\n"
            "Niveaux : Débutant, Facile, Intermédiaire, Avancé "
            "(quelques pièces dépassent le niveau moyen).\n\n"
        )
        fichier.write("| # | Durée | Titre | Compositeur | Niveau | Fichier |\n")
        fichier.write("|---|-------|-------|-------------|--------|---------|\n")

        numero = 1
        for duree, titre, compositeur, niveau, chemin in lignes:
            fichier.write(
                f"| {numero} | {formater_duree(duree)} | {titre} | "
                f"{compositeur} | {LIBELLES_NIVEAU[niveau]} | "
                f"`{chemin}` |\n"
            )
            numero += 1

        fichier.write(f"\n{len(lignes)} morceaux.\n")

        # Morceaux celebres encore manquants, a se procurer.
        fichier.write("\n## À ajouter (absents de la collection)\n\n")
        fichier.write(
            "Morceaux célèbres et accessibles qui manquent encore "
            "et qu'il serait utile d'ajouter.\n\n"
        )
        fichier.write("| Titre | Compositeur | Niveau |\n")
        fichier.write("|-------|-------------|--------|\n")
        for titre, compositeur, niveau in MANQUANTS:
            fichier.write(
                f"| {titre} | {compositeur} | "
                f"{LIBELLES_NIVEAU[niveau]} |\n"
            )


if __name__ == "__main__":
    print("** Génération de PLAYLIST.md")
    lignes = construire_lignes()
    ecrire_playlist(lignes)
    print(f"** Terminé : {len(lignes)} morceaux écrits")
