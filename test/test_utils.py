from dlchordx import const
from dlchordx.chord import Chord
from dlchordx.chord import __match_quality, tone_to_chords, interval_to_chords

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


def test_match_quality():
    for quality_name, notes in const.CHORD_MAP.items():
        _, quality = __match_quality(notes)
        assert quality_name == quality


def test_notes_to_chords():
    tones = tone_list
    qualities = const.CHORD_MAP.items()
    for quality_name, _ in qualities:
        for root_text in tones:
            for bass_text in tones:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)

                chord_list = tone_to_chords(chord.get_components()[0])
                assert chord_list[0] == chord


def test_note_indexes_to_chords():
    tones = tone_list
    qualities = const.CHORD_MAP.items()
    for quality_name, _ in qualities:
        for root_text in tones:
            for bass_text in tones:
                chord_name = root_text + quality_name + "/" + bass_text
                chord = Chord(chord_name)

                chord_list = interval_to_chords(chord.get_notes())
                assert chord_list[0] == chord


if __name__ == "__main__":
    test_match_quality()
    test_note_indexes_to_chords()
    test_notes_to_chords()
