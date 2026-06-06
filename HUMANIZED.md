# Fichiers humanisés

Fichiers MIDI retravaillés avec `enhance.py` pour leur donner du
relief. Les hauteurs ne sont jamais modifiées ; seules la dynamique,
le micro-timing et la pédale le sont.

## Humanisation de la vélocité

Fichiers dont la vélocité était uniforme (jeu robotique), humanisés
et remplacés en place dans la collection. La colonne Pédale indique
si le fichier possédait déjà une pédale (conservée telle quelle).

| Fichier | Vélocités après | Pédale d'origine |
|---|---|---|
| `BEETHOVEN LUDWIG VAN/Bagatelle in A Minor, WoO 59 (Für Elise).mid` | 34 | oui (440) |
| `ENFANTS CHILD/Aristide_Bruant_._Jeanneton.mid` | 37 | non |
| `ENFANTS CHILD/Cadet_Rousselle.mid` | 42 | non |
| `ENFANTS CHILD/Chanson_enfantine_._Pirouette.mid` | 37 | non |
| `ENFANTS CHILD/Fais_dodo_Colas_mon p_tit_frere.mid` | 37 | non |
| `ENFANTS CHILD/Il_court_le_furet.mid` | 41 | non |
| `ENFANTS CHILD/Il_etait_une_bergere.mid` | 37 | non |
| `ENFANTS CHILD/J_ai_du_bon_tabac.mid` | 37 | non |
| `ENFANTS CHILD/Malbrough_s_en va_t_en guerre.mid` | 37 | non |
| `ENFANTS CHILD/Ne_pleure_pas_Jeannette.mid` | 37 | non |
| `ENFANTS CHILD/Nous_n_irons_plus_au_bois.mid` | 37 | non |
| `ENFANTS CHILD/Trois_jeunes_tambours.mid` | 47 | non |
| `HALVORSEN JOHAN/Handel Passacaglia.mid` | 37 | oui (146) |
| `HAYDN FRANZ JOSEPH/Sonata No. 1 in G major, Hob. XVI8 (ca. 1755-60) 4. Allegro.mid` | 38 | non |
| `PIANO BAR/In my life.mid` | 37 | non |
| `POP-FRANCE/Il_était_une_fois_reve_d_elle2.mid` | 37 | non |
| `POP-FRANCE/Renaud-Mistral gagnant.mid` | 37 | non |
| `POP-FRANCE/Yann Tiersen - Comptine dun autre ete1.mid` | 37 | non |
| `POP-FRANCE/Yann Tiersen - Le Matin.mid` | 37 | non |
| `POP-INTER/Alan_Walker_Faded.mid` | 37 | non |
| `SATIE ERIK/Gymnopedie No - simple.mid` | 37 | non |
| `SCHUBERT FRANZ/Standchen (Serenade), D. 957 No. 4.mid` | 42 | oui (393) |

22 fichiers humanisés.

## Pédale ajoutée

Fichiers aux nuances correctes mais sans pédale, pédalisés
automatiquement (un coup de pédale par temps). Ils se trouvent dans
le dossier source et ne sont **pas encore intégrés** à la collection
(à écouter avant intégration ; Solfeggietto et Arabesque sont à
vérifier car ces pièces se jouent peu ou pas pédalées).

| Morceau | Compositeur | Sustain après |
|---|---|---|
| Menuet en sol (Petzold) | J.-S. Bach | 384 |
| Hymne à la joie (Ode to Joy) | L. van Beethoven | 192 |
| Arabesque, Op. 100 n°2 | F. Burgmüller | 774 |
| Solfeggietto | C. P. E. Bach | 270 |
| Canon en ré | J. Pachelbel | 360 |
| Valse, Op. 39 n°8 | P. I. Tchaïkovski | 506 |

6 fichiers pédalisés (dossier source).
