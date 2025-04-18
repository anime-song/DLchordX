from dlchordx import const
from dlchordx.parser import ChordParser
from dlchordx.chord import Tone


def test_parse():
    parser = ChordParser()
    for quality_name, _ in const.CHORD_MAP.items():
        for i in range(12):
            for j in range(12):
                root_tone = Tone("C").transpose(i)
                bass_tone = Tone("C").transpose(j)
                chord_name = root_tone.name + quality_name + "/" + bass_tone.name
                parser = ChordParser()
                chord_data = parser.parse(chord_name)
                assert root_tone.name == chord_data.root_text
                assert bass_tone.name == chord_data.bass_text
                assert quality_name == chord_data.quality_text


if __name__ == "__main__":
    test_parse()
