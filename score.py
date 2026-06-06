#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nom du fichier : score.py
Description : Génère une partition PDF pour chaque fichier MIDI de la
             collection, en parcourant récursivement les sous-dossiers.
             Chaque partition reçoit un en-tête avec le titre du morceau
             (nom du fichier) et le compositeur (nom du dossier parent).
             Les fichiers qui possèdent déjà un PDF sont ignorés.
Auteur : O. Booklage
Date : Juin 2026
Licence : CC BY-SA 4.0

Prérequis : MuseScore 3
    $ sudo apt install musescore3
"""

import os
import re
import sys
import glob
import json
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from subprocess import run, DEVNULL, TimeoutExpired


# Commande MuseScore 3 utilisée pour les conversions.
COMMANDE_MUSESCORE = "mscore3"

# Délai maximal (en secondes) accordé à MuseScore pour convertir un
# fichier. Certains fichiers figent MuseScore indéfiniment ; au-delà
# de ce délai, le processus est interrompu et le fichier est ignoré.
DELAI_MUSESCORE = 90

# Bornes de la taille de police du titre (en points). La taille est
# choisie selon la longueur du titre pour qu'il tienne sur une ligne :
# petite police pour les titres longs, plus grande pour les courts.
TAILLE_TITRE_MAX = 24
TAILLE_TITRE_MIN = 10

# Dossier racine analysé : celui qui contient ce script.
DOSSIER_RACINE = os.path.dirname(os.path.abspath(__file__))

# Particules de noms propres qui restent en minuscules, même au milieu
# d'un nom de compositeur (« Ludwig van Beethoven », « Manuel de Falla »).
PARTICULES = {
    "van", "von", "de", "du", "des", "la", "le", "di", "da",
    "del", "della", "der", "den", "ter", "ten", "y", "of",
}


def chemin_pdf(fichier_midi):
    """Construire le chemin du PDF associé à un fichier MIDI.

    Le PDF porte le même nom que le fichier MIDI et se trouve dans
    le même dossier (seule l'extension change).

    Args:
        fichier_midi: Chemin du fichier .mid.

    Returns:
        Le chemin du fichier .pdf correspondant.
    """
    dossier = os.path.dirname(fichier_midi)
    nom_sans_extension = Path(fichier_midi).stem
    return os.path.join(dossier, nom_sans_extension + ".pdf")


def lire_infos_sidecar(fichier_midi):
    """Lire le fichier d'informations JSON associé à un MIDI, s'il existe.

    Le sidecar porte le même nom que le MIDI, avec l'extension .json
    (voir infos.py).

    Args:
        fichier_midi: Chemin du fichier .mid.

    Returns:
        Le dictionnaire d'informations, ou None si le sidecar est
        absent ou illisible.
    """
    base, _ = os.path.splitext(fichier_midi)
    chemin = base + ".json"
    if not os.path.exists(chemin):
        return None
    try:
        with open(chemin, encoding="utf-8") as fichier:
            return json.load(fichier)
    except (ValueError, OSError):
        return None


def entete_partition(fichier_midi):
    """Déterminer le titre et la ligne d'artiste de l'en-tête.

    Si un sidecar JSON existe, on utilise score_title comme titre et
    "performer (date)" comme ligne d'artiste (la date entre parenthèses
    si elle est renseignée). Sinon, on retombe sur le nom du fichier et
    le nom du dossier.

    Args:
        fichier_midi: Chemin du fichier .mid.

    Returns:
        Un couple (titre, artiste) de chaînes.
    """
    infos = lire_infos_sidecar(fichier_midi)
    if infos:
        titre = infos.get("score_title") or titre_morceau(fichier_midi)
        artiste = infos.get("performer") or nom_compositeur(fichier_midi)
        date = str(infos.get("date", "")).strip()
        if date:
            artiste = f"{artiste} ({date})"
        return titre, artiste

    return titre_morceau(fichier_midi), nom_compositeur(fichier_midi)


def titre_morceau(fichier_midi):
    """Déduire le titre du morceau à partir du nom du fichier MIDI.

    Args:
        fichier_midi: Chemin du fichier .mid.

    Returns:
        Le nom du fichier sans son extension.
    """
    return Path(fichier_midi).stem


def formater_mot(mot):
    """Mettre en forme un mot d'un nom propre.

    Les particules (« van », « de »...) passent en minuscules, les
    autres mots prennent une majuscule initiale. Les traits d'union
    sont gérés morceau par morceau (« Cosma-Prevert »).

    Args:
        mot: Un mot du nom du dossier, en majuscules.

    Returns:
        Le mot mis en forme.
    """
    morceaux_formates = []
    for morceau in mot.split("-"):
        if morceau.lower() in PARTICULES:
            morceaux_formates.append(morceau.lower())
        else:
            morceaux_formates.append(morceau.capitalize())
    return "-".join(morceaux_formates)


def nom_compositeur(fichier_midi):
    """Déduire le nom du compositeur à partir du dossier parent.

    Le dossier suit la convention « NOM PRENOM [PARTICULE] ». On
    déplace le premier mot (le nom de famille) à la fin pour obtenir
    l'ordre de lecture courant, par exemple :
    « BEETHOVEN LUDWIG VAN » devient « Ludwig van Beethoven ».

    Args:
        fichier_midi: Chemin du fichier .mid.

    Returns:
        Le nom du compositeur mis en forme.
    """
    dossier = os.path.basename(os.path.dirname(fichier_midi))
    mots = dossier.split()

    # Déplacer le nom de famille (premier mot) en fin de chaîne.
    if len(mots) > 1:
        mots = mots[1:] + mots[:1]

    return " ".join(formater_mot(mot) for mot in mots)


def echapper_xml(texte):
    """Échapper les caractères spéciaux pour une insertion dans du XML.

    Args:
        texte: Le texte brut à insérer.

    Returns:
        Le texte avec les caractères &, < et > échappés.
    """
    texte = texte.replace("&", "&amp;")
    texte = texte.replace("<", "&lt;")
    texte = texte.replace(">", "&gt;")
    return texte


def taille_titre(titre):
    """Choisir une taille de police qui fait tenir le titre sur une ligne.

    La largeur d'un titre est à peu près proportionnelle au nombre de
    caractères multiplié par la taille de police. Pour une page A4, un
    facteur d'environ 1050 garde le titre dans les marges. La taille est
    bornée entre TAILLE_TITRE_MIN et TAILLE_TITRE_MAX.

    Args:
        titre: Le titre à afficher.

    Returns:
        La taille de police en points (entier).
    """
    longueur = max(len(titre), 1)
    taille = 1050 // longueur
    return max(TAILLE_TITRE_MIN, min(TAILLE_TITRE_MAX, taille))


def construire_cadre_titre(titre, compositeur):
    """Construire le cadre MuseScore (VBox) affichant l'en-tête.

    Le cadre contient deux textes : le titre du morceau et le nom du
    compositeur, dans les styles standards de MuseScore.

    Args:
        titre: Le titre du morceau.
        compositeur: Le nom du compositeur.

    Returns:
        Le fragment XML du cadre, prêt à être inséré dans le .mscx.
    """
    # On force une taille de police adaptée à la longueur du titre :
    # la valeur par défaut de MuseScore (~28pt) fait déborder les
    # titres longs hors de la page.
    titre_dimensionne = '<font size="' + str(taille_titre(titre)) + '"/>'
    titre_dimensionne += echapper_xml(titre)

    lignes = [
        "      <VBox>",
        "        <height>15</height>",
        "        <Text>",
        "          <style>Title</style>",
        "          <text>" + titre_dimensionne + "</text>",
        "        </Text>",
        "        <Text>",
        "          <style>Composer</style>",
        "          <text>" + echapper_xml(compositeur) + "</text>",
        "        </Text>",
        "        </VBox>",
        "",
    ]
    return "\n".join(lignes)


def ajouter_titre_compositeur(fichier_mscx, titre, compositeur):
    """Insérer le titre et le compositeur dans un fichier .mscx.

    On renseigne les métadonnées (workTitle, composer) et on ajoute
    un cadre titre visible au début de la première portée.

    Args:
        fichier_mscx: Chemin du fichier MuseScore à modifier.
        titre: Le titre du morceau.
        compositeur: Le nom du compositeur.
    """
    with open(fichier_mscx, encoding="utf-8") as fichier:
        contenu = fichier.read()

    # Renseigner les métadonnées (regex : le champ peut déjà être
    # rempli par l'import MIDI). Le remplacement par fonction évite tout
    # souci d'échappement des antislashs dans le titre.
    contenu = re.sub(
        r'<metaTag name="composer">.*?</metaTag>',
        lambda m: '<metaTag name="composer">'
        + echapper_xml(compositeur) + "</metaTag>",
        contenu, count=1, flags=re.DOTALL,
    )
    contenu = re.sub(
        r'<metaTag name="workTitle">.*?</metaTag>',
        lambda m: '<metaTag name="workTitle">'
        + echapper_xml(titre) + "</metaTag>",
        contenu, count=1, flags=re.DOTALL,
    )

    cadre = construire_cadre_titre(titre, compositeur)
    debut_portee = contenu.find('<Staff id="1">')
    if debut_portee != -1:
        # Supprimer un éventuel cadre titre (VBox) que MuseScore a déjà
        # créé depuis les métadonnées du MIDI, sinon le titre apparaît
        # en double.
        fin_entete = contenu.find("<Measure>", debut_portee)
        if fin_entete != -1:
            entete = contenu[debut_portee:fin_entete]
            entete = re.sub(
                r"[ \t]*<VBox>.*?</VBox>\s*", "", entete, flags=re.DOTALL
            )
            contenu = contenu[:debut_portee] + entete + contenu[fin_entete:]

        # Insérer notre cadre juste avant la première mesure.
        debut_mesure = contenu.find("<Measure>", debut_portee)
        if debut_mesure != -1:
            debut_ligne = contenu.rfind("\n", 0, debut_mesure) + 1
            contenu = (
                contenu[:debut_ligne] + cadre + contenu[debut_ligne:]
            )

    with open(fichier_mscx, "w", encoding="utf-8") as fichier:
        fichier.write(contenu)


def executer_musescore(fichier_entree, fichier_sortie):
    """Lancer MuseScore 3 pour convertir un fichier vers un autre format.

    QT_QPA_PLATFORM=offscreen permet à MuseScore de s'exécuter sans
    serveur graphique (utile en ligne de commande). Si MuseScore
    dépasse DELAI_MUSESCORE secondes (fichier qui le fige), le
    processus est interrompu et la conversion est considérée échouée.

    Args:
        fichier_entree: Chemin du fichier source.
        fichier_sortie: Chemin du fichier à produire.

    Returns:
        True si la conversion a réussi, False sinon (échec ou délai
        dépassé).
    """
    environnement = dict(os.environ, QT_QPA_PLATFORM="offscreen")
    try:
        resultat = run(
            [COMMANDE_MUSESCORE, fichier_entree, "-o", fichier_sortie],
            env=environnement,
            stdout=DEVNULL,
            stderr=DEVNULL,
            timeout=DELAI_MUSESCORE,
        )
    except TimeoutExpired:
        return False
    return resultat.returncode == 0


def generer_partition(fichier_midi, forcer=False):
    """Générer la partition PDF d'un fichier MIDI avec son en-tête.

    Le MIDI est d'abord converti en format MuseScore éditable (.mscx)
    pour y injecter le titre et le compositeur, puis exporté en PDF.
    Si le PDF existe déjà et que forcer vaut False, la génération est
    ignorée.

    Le PDF est d'abord produit dans un fichier temporaire, puis copié
    sur sa destination uniquement en cas de succès : un PDF existant
    n'est donc jamais perdu si la conversion échoue.

    Args:
        fichier_midi: Chemin du fichier .mid à convertir.
        forcer: Régénérer même si le PDF existe déjà.

    Returns:
        True si une partition a été générée, False si elle existait
        déjà ou si la conversion a échoué.
    """
    fichier_pdf = chemin_pdf(fichier_midi)
    if os.path.exists(fichier_pdf) and not forcer:
        return False

    # Fichiers intermédiaires, supprimés à la fin du traitement.
    descripteur_mscx, fichier_mscx = tempfile.mkstemp(suffix=".mscx")
    os.close(descripteur_mscx)
    descripteur_pdf, fichier_pdf_temporaire = tempfile.mkstemp(suffix=".pdf")
    os.close(descripteur_pdf)

    try:
        if not executer_musescore(fichier_midi, fichier_mscx):
            print(f"|!| Conversion impossible : {fichier_midi}")
            return False

        titre, compositeur = entete_partition(fichier_midi)
        ajouter_titre_compositeur(fichier_mscx, titre, compositeur)

        if not executer_musescore(fichier_mscx, fichier_pdf_temporaire):
            print(f"|!| Conversion impossible : {fichier_midi}")
            return False

        # La conversion a réussi : on remplace le PDF de destination.
        shutil.move(fichier_pdf_temporaire, fichier_pdf)
    finally:
        for fichier_temporaire in (fichier_mscx, fichier_pdf_temporaire):
            if os.path.exists(fichier_temporaire):
                os.remove(fichier_temporaire)

    return True


def trouver_fichiers_midi(dossier_racine):
    """Lister tous les fichiers .mid sous un dossier, récursivement.

    Args:
        dossier_racine: Dossier de départ de la recherche.

    Returns:
        La liste triée des chemins des fichiers .mid trouvés.
    """
    motif = os.path.join(dossier_racine, "**", "*.mid")
    return sorted(glob.glob(motif, recursive=True))


def main():
    """Parcourir la collection et générer les partitions.

    Sans argument, seules les partitions manquantes sont générées.
    Avec l'option --force, toutes les partitions sont régénérées
    (utile après un changement de mise en forme, par exemple l'ajout
    du titre et du compositeur en en-tête).
    """
    forcer = "--force" in sys.argv[1:]

    fichiers = trouver_fichiers_midi(DOSSIER_RACINE)
    total = len(fichiers)
    mode = "régénération complète" if forcer else "partitions manquantes"
    print(f"Génération des partitions ({mode}) pour {total} fichiers MIDI")

    nombre_generees = 0
    for index, fichier_midi in enumerate(fichiers, start=1):
        heure = datetime.now().strftime("%H:%M:%S")
        nom = os.path.relpath(fichier_midi, DOSSIER_RACINE)
        print(f"{index}/{total} {heure} {nom}")
        if generer_partition(fichier_midi, forcer=forcer):
            nombre_generees += 1

    print(f"** Terminé : {nombre_generees} partitions générées")


if __name__ == "__main__":
    main()
