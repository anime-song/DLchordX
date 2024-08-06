from typing import List
from dlchordx import Chord, Tone, Scale, get_scale

class ChordNode:
    def __init__(self, chord: Chord, prev_chord: Chord, next_chord: Chord):
        self.chord = chord
        self.prev_chord = prev_chord
        self.next_chord = next_chord

class ChordProg:
    def __init__(self, chord_list: List[Chord], major_key: str):
        self.chord_list = chord_list
        self.chord_nodes = self.__parse_chord_node(self.chord_list)
        self.major_key = Tone(major_key)

    def __parse_chord_node(self, chord_list: List[Chord]) -> List[ChordNode]:
        nodes = []
        for i, chord in enumerate(chord_list):
            if i == 0:
                prev_chord = None
            else:
                prev_chord = chord_list[i - 1]
            if i == len(chord_list) - 1:
                next_chord = None
            else:
                next_chord = chord_list[i + 1]

            node = ChordNode(chord, prev_chord=prev_chord, next_chord=next_chord)
            nodes.append(node)

        return nodes

    def modified_accidentals(self) -> List[Chord]:
        scale = get_scale(self.major_key, Scale.MAJOR)
        interval = self.major_key.get_interval_from(Tone("C"))
        scale = scale[-interval:] + scale[:-interval]

        result_chords = []
        for node in self.chord_nodes:
            chord = node.chord.modified_accidentals(self.major_key)
            if node.chord.quality.exists("dim"):
                # 上行の場合
                if node.next_chord and node.next_chord.bass.get_interval_from(node.chord.bass) == 1:
                    chord = node.chord.transpose(-1).modified_accidentals(self.major_key).transpose(1)
                # 下行の場合
                if node.next_chord and node.next_chord.bass.get_interval_from(node.chord.bass) == 11:
                    chord = node.chord.transpose(1).modified_accidentals(self.major_key).transpose(-1)

            if node.chord.bass.get_interval_from(self.major_key) == 6:
                if node.prev_chord.quality.exists("m") and node.prev_chord.bass.get_interval_from(self.major_key) == 1:
                    chord = node.chord.transpose(-1).modified_accidentals(self.major_key).transpose(1)

            result_chords.append(chord)
        return result_chords