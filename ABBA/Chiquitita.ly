% This LilyPond file was generated by Rosegarden 21.12
\include "nederlands.ly"
\version "2.6.0"
\header {
    copyright =  \markup { "Copyright "\char ##x00A9" xxxx Détenteur du copyright" }
    subtitle = "pas encore de sous-titre"
    title = "Pas encore de titre"
    tagline = "Created using Rosegarden 21.12 and LilyPond"
}
#(set-global-staff-size 32)
#(set-default-paper-size "a4")
global = { 
    \time 4/4
    \skip 1*102 
}
globalTempo = {
    \override Score.MetronomeMark #'transparent = ##t
    \tempo 4 = 86  \skip 1 
    \tempo 4 = 69  \skip 4 
    \tempo 4 = 72  \skip 4 
    \tempo 4 = 75  \skip 4 
    \tempo 4 = 78  \skip 4 
    \tempo 4 = 82  \skip 1*4 
    \tempo 4 = 85  \skip 4 \skip 2 \skip 1*90 \skip 2 
    \tempo 4 = 80  \skip 4 
    \tempo 4 = 74  \skip 4 
    \tempo 4 = 69  \skip 4 
    \tempo 4 = 64  \skip 4 
    \tempo 4 = 58  \skip 4 
    \tempo 4 = 52  \skip 4 
    \tempo 4 = 48  \skip 4 
    \tempo 4 = 41  
}
\score {
    << % common
        % Force offset of colliding notes in chords:
        \override Score.NoteColumn #'force-hshift = #1.0
        % Allow fingerings inside the staff (configured from export options):
        \override Score.Fingering #'staff-padding = #'()

        \context Staff = "track 1, Acoustic Grand Piano" << 
            \set Staff.instrument = \markup { \center-column { "Acoustic Grand Piano " } }
            \set Staff.midiInstrument = "Acoustic Grand Piano"
            \set Score.skipBars = ##t
            \set Staff.printKeyCancellation = ##f
            \new Voice \global
            \new Voice \globalTempo

            \context Voice = "voice 1" {
                % Segment: Acoustic Grand Piano
                \override Voice.TextScript #'padding = #2.0
                \override MultiMeasureRest #'expand-limit = 1
                \once \override Staff.TimeSignature #'style = #'() 
                \time 4/4
                
                \clef "alto"
                \key fis \major
                R1  |
                r4 < cis' e' > 8 < d' fis' d' > -\staccato < e' gis' e' > 32 -\tenuto r r fis' < fis' a' > 8 < gis' gis' b' > -\staccato < a' cis'' >  |
                < e' gis' b' > 2. r16 a' b' a' )  |
                < gis' b' > 16 -\tenuto e'' 2 -\tenuto r16 r8 fis' -\tenuto gis'  |
%% 5
                < e' fis' > 16 -\tenuto a' 2 r16 r8 fis' 8. r16  |
                < e' gis' b' > 4. -\tenuto b' 16 -\tenuto cis'' -\tenuto < fis'' d'' > 4 < fis'' d'' > -\tenuto  |
                a 16 e' gis' cis'' ) a e' gis' cis'' ) a fis' a' d'' ) a fis' a' d'' )  |
                a 16 e' gis' cis'' ) a -\tenuto e' gis' cis'' ) a fis' a' d'' ) a -\tenuto fis' a' d'' )  |
                < cis'' a > 16 e' gis' cis'' ) a e' gis' cis'' ) a fis' a' d'' ) a fis' a' d'' )  |
%% 10
                e' 16 a' cis'' ) a e' a' b' ) < cis'' a > -\tenuto e' a' cis'' ) < d'' a > fis' a' d'' ) 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 34560 + 3600 < 38400  &&  15/16 < 4/4
                r16  |
                < cis'' a > 8 b' < a' a > gis' ) e 16 b e' gis' ) e b e' gis' )  |
                e 16 b e' gis' ) e -\tenuto b e' gis' ) e b e' gis' ) e -\tenuto b e' gis' )  |
                < e'' e > 16 gis' b' e'' ) < gis' e > b' d'' e'' ) < fis'' d > a' d'' fis'' ) d a' d'' a' )  |
                e' 16 gis' b' ) e e' gis' a' ) < b' fis' e, > 2 -\tenuto 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 49920 + 3600 < 53760  &&  15/16 < 4/4
                r16  |
%% 15
                < a, fis' > 8 e' d' e' ) a 16 fis' a' d'' ) a fis' a' d'' )  |
                a 16 e' gis' cis'' ) a -\tenuto e' a' b' ) cis'' 8 -\tenuto d'' -\tenuto cis'' 16 -\tenuto b' -\tenuto a' 8 -\tenuto  |
                < cis'' a > 16 e' a' cis'' ) a e' a' cis'' ) a fis' a' d'' ) a fis' a' d'' )  |
                e' 16 a' cis'' ) a e' a' b' ) < cis'' a > -\tenuto e' a' cis'' ) < d'' a > fis' a' d'' ) 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 65280 + 3600 < 69120  &&  15/16 < 4/4
                r16  |
                < e'' cis > 16 gis' dis'' cis'' ) < e'' cis > gis' dis'' cis'' ) cis e' gis' cis'' ) cis -\tenuto e' gis' cis'' )  |
%% 20
                cis 16 e' gis' cis'' ) cis -\tenuto e' gis' cis'' ) cis e' gis' cis'' ) cis e' gis' cis'' )  |
                < e'' e > 16 gis' b' e'' ) < gis' e > b' d'' fis'' ) < a' d > -\tenuto d'' -\tenuto fis'' 8 < a' d > 16 d'' ) a' -\tenuto gis' -\tenuto  |
                < e' e > 16 -\tenuto gis' -\tenuto b' 8 < e' e > 16 gis' ) a' -\tenuto < b' fis' > -\tenuto e 2 -\tenuto  |
                < a, fis' > 8 e' d' e' ) a 16 fis' a' d'' ) a -\tenuto fis' a' d'' )  |
                a 16 e' gis' cis'' ) a -\tenuto e' a' b' ) cis'' 8 -\tenuto d'' -\tenuto cis'' 16 -\tenuto b' -\tenuto a' 8 -\tenuto  |
%% 25
                < cis'' a > 16 e' gis' cis'' ) a e' gis' cis'' ) a fis' a' d'' ) a fis' a' d'' )  |
                e' 16 a' cis'' ) a e' a' b' ) < cis'' a > -\tenuto e' a' cis'' ) < d'' a > fis' a' d'' ) 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 96000 + 3600 < 99840  &&  15/16 < 4/4
                r16  |
                < cis'' a > 8 b' < a' a > gis' ) e 16 b e' gis' ) e -\tenuto b e' gis' )  |
                e 16 b e' gis' ) e -\tenuto b e' gis' ) e b e' gis' ) e b e' gis' )  |
                < e'' e > 16 gis' b' e'' ) < gis' e > b' d'' e'' ) < fis'' d > a' d'' fis'' ) d a' d'' a' )  |
%% 30
                e' 16 gis' b' ) e e' gis' a' ) < b' fis' e, > 2 -\tenuto 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 111360 + 3600 < 115200  &&  15/16 < 4/4
                r16  |
                < a, fis' > 8 e' d' e' ) a 16 fis' a' d'' ) a -\tenuto fis' a' d'' )  |
                a 16 e' gis' cis'' ) a -\tenuto e' a' b' ) cis'' 8 -\tenuto d'' -\tenuto cis'' 16 -\tenuto b' -\tenuto a' 8 -\tenuto  |
                < cis'' a > 16 e' a' cis'' ) a e' a' cis'' ) a -\tenuto fis' a' d'' ) a fis' a' d'' )  |
                e' 16 a' cis'' ) a e' a' b' ) < cis'' a > e' a' cis'' ) < d'' a > fis' a' d'' ) 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 126720 + 3600 < 130560  &&  15/16 < 4/4
                r16  |
%% 35
                < e'' cis > 16 gis' dis'' cis'' ) < e'' cis > gis' dis'' cis'' ) cis e' gis' cis'' ) cis -\tenuto e' gis' cis'' )  |
                cis 16 e' gis' cis'' ) cis -\tenuto e' gis' cis'' ) cis e' gis' cis'' ) cis e' gis' cis'' )  |
                < e'' e > 16 gis' b' e'' ) < gis' e > b' d'' fis'' ) < a' d > -\tenuto d'' -\tenuto fis'' 8 < a' d > 16 d'' ) a' -\tenuto gis' -\tenuto  |
                < e' e > 16 -\tenuto gis' -\tenuto b' 8 < e' e > 16 gis' ) a' -\tenuto < b' fis' > -\tenuto e 2 -\tenuto  |
                < fis' a, > 8 e' d' e' ) a 16 fis' a' d'' ) a -\tenuto fis' a' d'' )  |
%% 40
                < a a, > 16 e' gis' cis'' ) a -\tenuto e' fis'' gis'' ) a'' 8 -\tenuto b'' -\tenuto a'' 16 gis'' fis'' gis'' )  |
                < a' fis' d' > 8 < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > 8 
                % avertissement: une mesure anormalement longue a été tronquée |
                                \once \override Staff.TimeSignature #'style = #'() 
                \time 5/4
                < a' fis' d' > 8 < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
                                \once \override Staff.TimeSignature #'style = #'() 
                \time 4/4
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
%% 45
                < gis' e' b > 8 < gis' e' b > < gis' e' b > < gis' e' b > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
                < gis' e' b > 8 < gis' e' b > < gis' e' b > < gis' e' b > < gis' e' b > < gis' e' b > < gis' e' b > < gis' e' b >  |
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
                < a' fis' d' > 8 < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
%% 50
                \skip 64  |
                                \once \override Staff.TimeSignature #'style = #'() 
                \time 5/4
                < a' fis' d' > 8 < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
                                \once \override Staff.TimeSignature #'style = #'() 
                \time 4/4
                < a' e' cis' > 8 < a' e' cis' > < e' a' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
                < e' a' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
                < gis' e' b > 8 < gis' e' b > < gis' e' b > < gis' e' b > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
%% 55
                < e' b gis' > 8 < e' gis' b > < b e' gis' > < b e' gis' > < e' gis' b fis' > < e' gis' b fis' > < gis' e' b fis' > < gis' e' fis' b >  |
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < cis' a > < b d' > )  |
                < e' e > 8 < fis' fis > < gis' gis > < a' a > ) < b b' > 4. -\tenuto < a a' > 8 -\tenuto  |
                < gis' e' b > 8 < gis' e' b > < gis' e' b > < gis' e' b > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
                < gis' e' b > 8 < gis' e' b > < gis' e' b > < gis' e' b > < b e' fis' > 2 -\tenuto  |
%% 60
                a 16 e' gis' cis'' ) a -\tenuto e' gis' cis'' ) a fis' a' d'' ) a fis' a' d'' )  |
                a 16 e' gis' cis'' ) a e' gis' cis'' ) a -\tenuto fis' a' d'' ) a fis' a' d'' )  |
                e' 16 gis' cis'' ) a e' gis' cis'' ) a fis' a' d'' ) a fis' a' d'' ) 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 232320 + 3600 < 236160  &&  15/16 < 4/4
                r16  |
                a 16 -\tenuto e' a' cis'' a -\tenuto e' a' b' < cis'' a > -\tenuto e' a' cis'' < d'' a > -\tenuto fis' a' d''  |
                < cis'' a > 8 -\tenuto b' < a' a > -\tenuto gis' -\tenuto e 16 b e' gis' ) e b e' gis' )  |
%% 65
                e 16 b e' gis' ) e b e' gis' ) e -\tenuto b e' gis' ) e b e' gis' )  |
                gis' 16 b' e'' ) < gis' e > b' d'' e'' ) < fis'' d > a' d'' fis'' ) d a' d'' a' ) 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 247680 + 3600 < 251520  &&  15/16 < 4/4
                r16  |
                < gis' e > 16 e' gis' b' ) e e' gis' a' ) < b' fis' e, > 2  |
                < a, fis' > 8 -\tenuto e' d' e' -\tenuto a 16 fis' a' d'' ) a fis' a' d'' )  |
                a 16 e' gis' cis'' ) a e' a' b' ) cis'' 8 d'' cis'' 16 -\tenuto b' -\tenuto a' 8  |
%% 70
                e' 16 a' cis'' ) a e' a' cis'' ) a fis' a' d'' ) a fis' a' d'' ) 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 263040 + 3600 < 266880  &&  15/16 < 4/4
                r16  |
                a 16 e' a' cis'' ) a -\tenuto e' a' b' ) < cis'' a > e' a' cis'' ) < d'' a > -\tenuto fis' a' d'' )  |
                < e'' cis > 16 gis' dis'' cis'' ) < e'' cis > -\tenuto gis' dis'' cis'' ) cis e' gis' cis'' ) cis e' gis' cis'' )  |
                cis 16 e' gis' cis'' ) cis e' gis' cis'' ) cis -\tenuto e' gis' cis'' ) cis e' gis' cis'' )  |
                gis' 16 b' e'' ) < gis' e > b' d'' fis'' ) < a' d > -\tenuto d'' -\tenuto fis'' 8 -\staccato < a' d > 16 d'' ) a' -\tenuto gis' -\tenuto 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 278400 + 3600 < 282240  &&  15/16 < 4/4
                r16  |
%% 75
                < e' e > 16 -\tenuto gis' -\tenuto b' 8 -\staccato < e' e > 16 gis' ) a' -\tenuto < b' fis' > -\tenuto e 2  |
                < fis' a, > 8 -\tenuto e' d' e' -\tenuto a 16 fis' a' d'' ) a fis' a' d'' )  |
                < a a, > 16 e' gis' cis'' ) a e' fis'' gis'' ) a'' 8 -\tenuto b'' -\tenuto a'' 16 gis'' fis'' gis'' )  |
                < a' fis' d' > 8 < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
                                \once \override Staff.TimeSignature #'style = #'() 
                \time 5/4
                < a' fis' d' > 8 < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
%% 80
                                \once \override Staff.TimeSignature #'style = #'() 
                \time 4/4
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
                < gis' e' b > 8 < gis' e' b > < gis' e' b > < gis' e' b > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
                < gis' e' b > 8 < gis' e' b > < gis' e' b > < gis' e' b > < gis' e' b > < gis' e' b > < gis' e' b > < gis' e' b >  |
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
%% 85
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
                < a' fis' d' > 8 < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > 8 
                % avertissement: une mesure anormalement longue a été tronquée |
                                \once \override Staff.TimeSignature #'style = #'() 
                \time 5/4
                < a' fis' d' > 8 < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
                \skip 64  |
                                \once \override Staff.TimeSignature #'style = #'() 
                \time 4/4
                < a' e' cis' > 8 < a' e' cis' > < e' a' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
%% 90
                < e' a' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' >  |
                < gis' e' b > 8 < gis' e' b > < gis' e' b > < gis' e' b > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
                < e' b gis' > 8 < e' gis' b > < b e' gis' > < b e' gis' > < e' gis' b fis' > < e' gis' b fis' > < gis' e' b fis' > < gis' e' fis' b >  |
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < cis' a > < b d' > )  |
                < fis' fis > 8 < gis' gis > < a' a > ) < b b' > 4. -\tenuto < a a' > 8 -\tenuto 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 353280 + 3360 < 357120  &&  7/8 < 4/4
                r8  |
%% 95
                < gis' e' b > 8 < gis' e' b > < gis' e' b > < gis' e' b > < a' fis' d' > < a' fis' d' > < a' fis' d' > < a' fis' d' >  |
                < gis' e' b > 8 < gis' e' b > < gis' e' b > < gis' e' b > < b e' fis' > 2 -\tenuto  |
                < a' e' cis' > 8 < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < a' e' cis' > < cis' a > < b d' > )  |
                < fis' fis > 8 < gis' gis > < a' a > ) < b' b > 4. -\tenuto < a a' > 8 -\tenuto 
                % avertissement: une mesure trop courte a été complétée par des silences
                % 368640 + 3360 < 372480  &&  7/8 < 4/4
                r8  |
                < gis' e' b > 2 -\tenuto < d' fis' a' > -\tenuto  |
%% 100
                < b e' gis' > 1 -\tenuto  |
                fis' 8 -\tenuto e' -\tenuto d' -\tenuto cis' 4. -\tenuto r4  |
                R1*2  |
                \bar "|."
            } % Voice
        >> % Staff (final) ends

    >> % notes

    \layout {
        indent = 3.0\cm
        short-indent = 1.5\cm
        \context { \Staff \RemoveEmptyStaves }
        \context { \GrandStaff \accepts "Lyrics" }
    }
%     uncomment to enable generating midi file from the lilypond source
%         \midi {
%             \tempo 4 = 86
%         } 
} % score
