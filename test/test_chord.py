import copy

from dlchordx import const
from dlchordx.chord import Chord, Tone

tone_list = [
    "C",
    "B#",
    "Dbb",
    "Db",
    "C#",
    "D",
    "Ebb",
    "C##",
    "Eb",
    "D#",
    "E",
    "D##",
    "Fb",
    "F",
    "E#",
    "Gb",
    "F#",
    "G",
    "F##",
    "Abb",
    "Ab",
    "G#",
    "A",
    "G##",
    "Bbb",
    "Bb",
    "A#",
    "B",
    "Cb",
]


def test_root():
    for quality_name, _ in const.CHORD_MAP.items():
        for root_text in tone_list:
            for bass_text in tone_list:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)
                assert Tone(root_text) == chord.root


def test_bass():
    for quality_name, _ in const.CHORD_MAP.items():
        for root_text in tone_list:
            for bass_text in tone_list:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)
                assert Tone(bass_text) == chord.bass


def test_quality():
    for quality_name, _ in const.CHORD_MAP.items():
        for root_text in tone_list:
            for bass_text in tone_list:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)
                assert quality_name == chord.quality.name


def test_is_on_chord():
    for quality_name, _ in const.CHORD_MAP.items():
        for root_text in tone_list:
            for bass_text in tone_list:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)
                is_on_chord = Tone(root_text) != Tone(bass_text)
                assert is_on_chord == chord.is_on_chord

    for quality_name, _ in const.CHORD_MAP.items():
        for root_text in tone_list:
            chord_name = root_text + quality_name
            chord = Chord(chord_name)
            assert not chord.is_on_chord


def test_transpose():
    tones = tone_list
    qualities = const.CHORD_MAP.items()
    for quality_name, _ in qualities:
        for root_text in tones:
            for bass_text in tones:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)

                for i in range(1):
                    transposed_chord = chord.transpose(i)
                    transposed_chord_name = (
                        Tone(root_text).transpose(i).name
                        + quality_name
                        + "/"
                        + Tone(bass_text).transpose(i).name
                    )
                    transposed_chord_origin = Chord(transposed_chord_name)

                    assert transposed_chord_origin == transposed_chord


def test_get_notes():
    tones = tone_list
    qualities = const.CHORD_MAP.items()
    for quality_name, notes in qualities:
        for root_text in tones:
            for bass_text in tones:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)

                note_indexes = {note for note in chord.get_notes()}
                notes_origin = list(copy.copy(notes))

                for i in range(len(notes_origin)):
                    notes_origin[i] += Tone(root_text).get_interval()
                    notes_origin[i] %= 12

                if chord.is_on_chord:
                    notes_origin.insert(0, Tone(bass_text).get_interval())

                assert set(notes_origin) == note_indexes


def test_reconfigured():
    tones = tone_list
    qualities = const.CHORD_MAP.items()
    for quality_name, _ in qualities:
        for root_text in tones:
            for bass_text in tones:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)
                rec_chord = chord.reconfigured()
                assert chord == rec_chord


if __name__ == "__main__":
    test_bass()
    test_get_notes()
    test_is_on_chord()
    test_quality()
    test_reconfigured()
    test_root()
    test_transpose()
