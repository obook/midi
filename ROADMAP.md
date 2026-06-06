# Roadmap

This document records the current state of the collection's tooling and the
observations gathered while building it, so the next work session can pick up
where this one left off.

## Current state

The repository holds a large MIDI collection (about 1,377 files) with three
Python tools at its root:

- **infos.py** generates a JSON sidecar next to each MIDI (`piece.mid` ->
  `piece.json`). JSON keys are in English; the code and comments are in French.
  Each sidecar carries the title, score title, composer, performer, date,
  duration, humanized flag, pedal data, note count, tempo, and time signature.
  The three hand-editable fields (`score_title`, `performer`, `date`) are
  preserved on every re-run.
- **score.py** engraves a PDF for each MIDI with MuseScore 3. When a sidecar
  exists, the header uses `score_title` as the title and `performer (date)` as
  the artist line. The title font size adapts to the title length, and any
  title frame that MuseScore creates from embedded MIDI metadata is removed to
  avoid a duplicate title.
- **enhance.py** adds expressive pedaling and humanization, and **playlist.py**
  generates PLAYLIST.md.

Roughly 1,375 sidecars were produced (two MIDI files fail to parse), 1,220
dates were filled in (88 percent), about 1,008 score titles were normalized,
and all 1,377 scores were regenerated with the new header.

## Known limitations

- **Engraving quality.** Only "Fur Elise" is engraved from a quantized copy.
  Every other score is rendered straight from a humanized performance MIDI, so
  the rhythms are often dense and hard to read (tuplets, dotted figures, many
  rests). The header is correct everywhere, but the notation is not concert
  grade.
- **Missing dates.** About 155 pieces still have an empty date. Most are
  genuinely undatable: anonymous traditional tunes, children's songs, and
  personal hobbyist files with cryptic names. A few are real works that the
  research agents flagged as low confidence and that we deliberately left blank
  rather than guess.
- **Composer name for category folders.** The composer and performer are
  derived from the folder name with a first-name/last-name reorder, which is
  correct for people ("BEETHOVEN LUDWIG VAN" -> "Ludwig van Beethoven") but
  wrong for category folders ("ENFANTS CHILD" -> "Child Enfants",
  "BOSSA NOVA" -> "Nova Bossa").
- **Title language and accents.** The title research returned canonical English
  catalog titles, which dropped some non-French accents (for example "espanola"
  instead of the correct "española"). French titles keep their accents
  correctly.
- **A crashing source file.** `HUMMEL JOHAN NEPOMUK/Piano Sonata in F sharp
  Opus.81, Mov.2.mid` freezes MuseScore 3 indefinitely. score.py guards against
  this with a 90-second timeout per file, but the file itself still produces no
  usable score.
- **Two unreadable MIDIs.** Two files fail to parse in mido (a malformed key
  signature), so they have no sidecar and no refreshed metadata.

## Proposed next steps

1. **Optional quantization for engraving.** Add a tool (or a score.py flag) that
   engraves from a quantized copy of each MIDI, the way "Fur Elise" was handled.
   This would turn the whole collection into readable notation. The grid must be
   chosen per piece, since a fixed grid would distort works with triplets or
   fast passages.
2. **Special-case category folders.** Maintain a small list of folders that are
   not personal names (children's songs, film music, pop categories) and skip
   the first-name/last-name reorder for them.
3. **Fill the remaining datable pieces.** A focused pass on the few low-
   confidence entries (Bach toccatas, the Carmen Variations, and similar) could
   recover a handful more dates. The true traditional tunes should stay blank.
4. **Restore non-French accents in titles.** A light correction pass could put
   back Spanish and other accents that the catalog titles dropped.
5. **Decide what to do with the crashing and unreadable files.** Either repair
   them, replace them with clean versions, or mark them as known exclusions.
6. **Let score_title drive more.** The clean titles could also feed a catalog
   export (CSV or a web index) or a consistent renaming scheme, since the file
   names remain noisy.

## Gotchas for future sessions

- score.py writes the PDF to a temporary file first and only moves it into place
  on success, so a timeout or crash never destroys an existing PDF.
- The full regeneration takes roughly 30 to 45 minutes and produces a very large
  commit (more than 1,300 binary PDFs).
- Python buffers stdout when it is redirected to a file, so a background log can
  look frozen while the job is in fact still running. Check the live mscore3
  process or the recently modified PDFs instead of the log.
