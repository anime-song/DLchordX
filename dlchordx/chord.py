from __future__ import annotations
from dlchordx.parser import ChordParser, QualityParser
from dlchordx import const

from typing import List
from enum import Enum

simplified_sharp_scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
simplified_flat_scale = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
# W W H W W W H
major_scale_steps = [2, 2, 1, 2, 2, 2]
minor_scale_steps = [2, 1, 2, 2, 1, 2]

class Scale(Enum):
    MAJOR = 1
    MINOR = 2

class AccidentalType(Enum):
    SHARP = 1
    FLAT = 2
    NONE = 3

class Tone:
    def __init__(self, name: str):
        self.name = name
        self.name_without_accidentals = self.name.replace("#", "").replace("b", "")
        if self.name.count("b") > 0 and self.name.count("#") > 0:
            raise ValueError("臨時記号の種類は一つのみにする必要があります")

        if self.name.count("b") > 2 and self.name.count("#") > 2:
            raise ValueError("ダブルシャープ、ダブルフラット以上は対応していません")

        if self.name.count("b") > 0:
            self.accidental_type = AccidentalType.FLAT
        elif self.name.count("#") > 0:
            self.accidental_type = AccidentalType.SHARP
        else:
            self.accidental_type = AccidentalType.NONE

        self.interval_map = {
            "C": 0,
            "D": 2,
            "E": 4,
            "F": 5,
            "G": 7,
            "A": 9,
            "B": 11
        }

    @staticmethod
    def create_from_interval(interval: int) -> Tone:
        return Tone(simplified_flat_scale[interval])

    def __eq__(self, other: Tone) -> bool:
        if not isinstance(other, Tone):
            raise TypeError("{} オブジェクトとToneオブジェクトを比較できません。".format(type(other)))

        if self.get_interval() == other.get_interval():
            return True

        return False

    def __ne__(self, other: Tone) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<Tone: {}>".format(self.name)

    def get_interval(self) -> int:
        if self.accidental_type == AccidentalType.FLAT:
            interval_change = -self.name.count("b")
        elif self.accidental_type == AccidentalType.SHARP:
            interval_change = self.name.count("#")
        else:
            interval_change = 0

        interval = (self.interval_map[self.name_without_accidentals] + interval_change) % 12
        return interval

    def get_interval_from(self, other_tone: Tone) -> int:
        if other_tone.get_interval() > self.get_interval():
            return abs(other_tone.get_interval() - (self.get_interval() + 12))
        else:
            return abs(other_tone.get_interval() - self.get_interval())

    def get_min_interval_from(self, other_tone: Tone) -> int:
        interval = abs(self.get_interval() - other_tone.get_interval())
        return min(abs(12 - interval), interval)

    def simplify(self, advanced=False) -> Tone:
        if advanced:
            if self.name == "B#" or self.name == "Cb" or self.name == "E#" or self.name == "Fb":
                return Tone(self.name)

        if self.accidental_type == AccidentalType.SHARP:
            return Tone(simplified_sharp_scale[self.get_interval()])
        else:
            return Tone(simplified_flat_scale[self.get_interval()])

    def to_sharp_scale(self) -> Tone:
        return Tone(simplified_sharp_scale[self.get_interval()])

    def to_flat_scale(self) -> Tone:
        return Tone(simplified_flat_scale[self.get_interval()])

    def transpose(self, steps) -> Tone:
        negative = True if steps < 0 else False
        steps = -1 * steps if negative else steps

        result_tone = self
        # simplified_tone = self.simplify(advanced=True)
        for _ in range(steps):
            if negative:
                if "##" in result_tone.name:
                    transposed_tone = Tone(result_tone.name_without_accidentals + "#")
                elif "#" in result_tone.name:
                    transposed_tone = Tone(result_tone.name_without_accidentals)
                elif "bb" in result_tone.name:
                    transposed_tone = Tone(result_tone.simplify().name + "b")
                else:
                    transposed_tone = Tone(result_tone.name + "b")
            else:
                if "bb" in result_tone.name:
                    transposed_tone = Tone(result_tone.name_without_accidentals + "b")
                elif "b" in result_tone.name:
                    transposed_tone = Tone(result_tone.name_without_accidentals)
                elif "##" in result_tone.name:
                    transposed_tone = Tone(result_tone.simplify().name + "#")
                else:
                    transposed_tone = Tone(result_tone.name + "#")

            result_tone = transposed_tone

        return result_tone

    def modified(self, major_key: str | Tone) -> Tone:
        if isinstance(major_key, Tone):
            base_tone = major_key
        else:
            base_tone = Tone(major_key)
        scale = get_scale(base_tone, Scale.MAJOR)
        interval = base_tone.get_interval_from(Tone("C"))
        shift_scale = scale[-interval:] + scale[:-interval]
        return shift_scale[self.get_interval()]



class DeleteInterval:
    THIRD = 1
    FIFTH = 2

class ChordTone:
    def __init__(self,
                 name: str,
                 base_interval: int,
                 interval_change: int = 0,
                 delete_interval: DeleteInterval = None,
                 conflict_chord_tones: List[str] = []):
        self.name = name
        self.base_interval = base_interval
        self.interval_change = interval_change
        self.delete_interval = delete_interval
        self.conflict_chord_tones = conflict_chord_tones

    def __eq__(self, other: ChordTone) -> bool:
        if not isinstance(other, ChordTone):
            raise TypeError("{} オブジェクトとChordToneオブジェクトを比較できません。".format(type(other)))

        if self.name == other.name:
            return True

        return False

    def __ne__(self, other: ChordTone) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<ChordTone: {}>".format(self.name)

    @staticmethod
    def create_from_name(name: str) -> ChordTone:
        for chord_tone in chord_tone_list:
            if chord_tone.name == name:
                return chord_tone

        return None

    def is_conflict(self, other_tone: ChordTone) -> bool:
        return other_tone.name in self.conflict_chord_tones

    def to_tone(self, base_tone: Tone) -> Tone:
        transposed_tone = base_tone.transpose(self.base_interval).modified(base_tone.name)
        if self.interval_change != 0:
            transposed_tone = transposed_tone.transpose(self.interval_change)
            return transposed_tone
        else:
            return transposed_tone

class ChordBaseQualityType(Enum):
    MAJOR = 1
    MINOR = 2
    DIMINISHED = 3
    AUGMENTED = 4

class ChordBaseQuality:
    def __init__(self, type: ChordBaseQualityType, interval_change=(0, 0, 0)):
        self.type = type
        self.interval_change = interval_change

chord_tone_list: List[ChordTone] = [
    ChordTone("sus2", base_interval=2,  interval_change=0,  delete_interval=DeleteInterval.THIRD, conflict_chord_tones=["9"]),
    ChordTone("2",    base_interval=2,  interval_change=0,  conflict_chord_tones=["9"]),
    ChordTone("sus4", base_interval=5,  interval_change=0,  delete_interval=DeleteInterval.THIRD, conflict_chord_tones=["11"]),
    ChordTone("4",    base_interval=5,  interval_change=0,  conflict_chord_tones=["11"]),
    ChordTone("b5",   base_interval=7,  interval_change=-1, delete_interval=DeleteInterval.FIFTH, conflict_chord_tones=["5", "#11"]),
    ChordTone("5",    base_interval=7,  interval_change=0,  delete_interval=DeleteInterval.THIRD, conflict_chord_tones=["b5", "#11"]),
    ChordTone("#5",   base_interval=7,  interval_change=+1, delete_interval=DeleteInterval.FIFTH, conflict_chord_tones=["5", "b13"]),
    ChordTone("6",    base_interval=9,  interval_change=0,  conflict_chord_tones=["13", "b13", "#5"]),
    ChordTone("7",    base_interval=11, interval_change=-1, conflict_chord_tones=["M7"]),
    ChordTone("M7",   base_interval=11, interval_change=0,  conflict_chord_tones=["7"]),
    ChordTone("b9",   base_interval=14, interval_change=-1, conflict_chord_tones=["9"]),
    ChordTone("9",    base_interval=14, interval_change=0,  conflict_chord_tones=["b9", "#9"]),
    ChordTone("#9",   base_interval=14, interval_change=+1, conflict_chord_tones=["9"]),
    ChordTone("11",   base_interval=17, interval_change=0,  conflict_chord_tones=["#11"]),
    ChordTone("#11",  base_interval=17, interval_change=+1, conflict_chord_tones=["11"]),
    ChordTone("13",   base_interval=21, interval_change=0,  conflict_chord_tones=["b13", "#5"]),
    ChordTone("b13",  base_interval=21, interval_change=-1, conflict_chord_tones=["13"]),
]

chord_base_quality_list = {
    ChordBaseQualityType.MAJOR: ChordBaseQuality(ChordBaseQualityType.MAJOR, interval_change=(0, 0, 0)),
    ChordBaseQualityType.MINOR: ChordBaseQuality(ChordBaseQualityType.MINOR, interval_change=(0, -1, 0)),
    ChordBaseQualityType.AUGMENTED:ChordBaseQuality(ChordBaseQualityType.AUGMENTED, interval_change=(0, 0, +1)),
    ChordBaseQualityType.DIMINISHED:ChordBaseQuality(ChordBaseQualityType.DIMINISHED, interval_change=(0, -1, -1)),
}

def get_scale(base_tone: Tone, scale: Scale) -> List[Tone]:
    if scale == Scale.MAJOR:
        scale_steps = major_scale_steps
    elif scale == Scale.MINOR:
        scale_steps = minor_scale_steps

    if base_tone.accidental_type == AccidentalType.SHARP:
        base_scale = get_scale(Tone(base_tone.name_without_accidentals), scale=scale)
        return [tone.transpose(base_tone.name.count("#")) for tone in base_scale]

    elif base_tone.accidental_type == AccidentalType.FLAT:
        base_scale = get_scale(Tone(base_tone.name_without_accidentals), scale=scale)
        return [tone.transpose(-base_tone.name.count("b")) for tone in base_scale]


    scales: List[Tone] = []
    current_tone = base_tone
    scales.append(current_tone)
    # 基本的なスケール内の音を追加
    for steps in scale_steps:
        current_tone = current_tone.transpose(steps).simplify()
        scales.append(current_tone)

    result_scales = [scales[0]]
    # 臨時記号を修正
    for tone in scales[1:]:
        tone_name_list = [t.name_without_accidentals for t in result_scales]
        has_duplicates = tone_name_list.count(tone.name_without_accidentals)
        if has_duplicates:
            if tone.accidental_type == AccidentalType.SHARP:
                tone = tone.to_flat_scale()
            elif tone.accidental_type == AccidentalType.FLAT:
                tone = tone.to_sharp_scale()
            else:
                flat_scale_tone = tone.to_flat_scale()
                sharp_scale_tone = tone.to_sharp_scale()
                if tone_name_list.count(flat_scale_tone.name_without_accidentals) == 0:
                    tone = flat_scale_tone
                elif tone_name_list.count(sharp_scale_tone.name_without_accidentals) == 0:
                    tone = sharp_scale_tone

        result_scales.append(tone)

    # 半音の音を追加
    indexes = [tone.get_interval() for tone in result_scales]
    indexes_roll = indexes[1:] + indexes[:1]
    index_intervals = [min(12 - abs(idx1 - idx2), abs(idx1 - idx2)) for idx1, idx2 in zip(indexes, indexes_roll)]

    semi_tone_changes = {
        1: AccidentalType.FLAT,
        3: AccidentalType.FLAT,
        4: AccidentalType.NONE,
        5: AccidentalType.SHARP,
        6: AccidentalType.SHARP,
        7: AccidentalType.FLAT,
        8: AccidentalType.FLAT,
        9: AccidentalType.NONE,
        10: AccidentalType.FLAT,
        11: AccidentalType.SHARP,
    }
    for i, interval in enumerate(index_intervals):
        if interval == 2:
            semi_tone = result_scales[i].transpose(1)
            base_tone_interval = semi_tone.get_interval_from(result_scales[0])
            accidental_type = semi_tone_changes[base_tone_interval]

            if accidental_type == AccidentalType.SHARP:
                semi_tone = semi_tone.to_sharp_scale()
            elif accidental_type == AccidentalType.FLAT:
                semi_tone = semi_tone.to_flat_scale()
            else:
                semi_tone = semi_tone.simplify()

            result_scales.append(semi_tone)
    result_scales = sorted(result_scales, key=lambda x: (x.get_interval() - result_scales[0].get_interval()) % 12)
    modified_scales = [result_scales[0]]
    for i, tone in enumerate(result_scales[1:]):
        high_tone = Tone(tone.name_without_accidentals)
        low_tone = Tone(result_scales[i].name_without_accidentals)
        if high_tone.get_min_interval_from(low_tone) >= 2:
            modified_scales.append(tone.simplify())
        else:
            modified_scales.append(tone)
    return modified_scales

def to_chord_tone(text: str) -> ChordTone:
    for chord_tone in chord_tone_list:
        if chord_tone.name == text.replace("-", "b").replace("+", "#").replace("add", ""):
            return chord_tone
    return None

def to_base_quality(text: str) -> ChordBaseQuality:
    if text == "m":
        return chord_base_quality_list[ChordBaseQualityType.MINOR]
    elif text == "aug":
        return chord_base_quality_list[ChordBaseQualityType.AUGMENTED]
    elif text == "dim":
        return chord_base_quality_list[ChordBaseQualityType.DIMINISHED]

    return None


class Quality:
    def __init__(self, quality_text: str):
        self.__name = quality_text
        parser = QualityParser()
        self.__quality_data = parser.parse(quality_text)

        self.__tones = [to_chord_tone(tone)
                        for tone in self.__quality_data.tones]
        self.__tones_parentheses = [to_chord_tone(tone)
                                    for tone in self.__quality_data.tones_parentheses]
        self.__add_tones = [to_chord_tone(tone) for tone in self.__quality_data.tones if "add" in tone]
        self.__base_qualities = [to_base_quality(quality) for quality in self.__quality_data.qualities]
        if not self.__base_qualities:
            self.__base_qualities.append(chord_base_quality_list[ChordBaseQualityType.MAJOR])

    def __str__(self) -> str:
        return self.__name

    def __repr__(self) -> str:
        return "<Quality: {}>".format(self.__name)

    def __eq__(self, other: Quality) -> bool:
        if not isinstance(other, Quality):
            raise TypeError("{} オブジェクトとQualityオブジェクトを比較できません".format(type(other)))
        return self.name == other.name

    def __ne__(self, other: Quality) -> bool:
        return not self.__eq__(other)

    @property
    def name(self) -> str:
        """
        生のクオリティテキストを取得します。
        :return: 生のクオリティテキスト
        """
        return self.__name

    @property
    def qualities(self) -> List[ChordBaseQuality]:
        """
        クオリティのリストを取得します。
        :return: クオリティのリスト
        """
        return self.__base_qualities

    @property
    def parent_tones(self) -> List[ChordTone]:
        """
        括弧内の構成音のリストを取得します。
        :return: 括弧内の構成音のリスト
        """
        return self.__tones_parentheses

    @property
    def tones(self) -> List[ChordTone]:
        """
        括弧外の構成音のリストを取得します。
        :return: 括弧外の構成音のリスト
        """
        return self.__tones

    @property
    def add_tones(self) -> List[ChordTone]:
        """
        addで追加された構成音を取得します
        """
        return self.__add_tones

    def exists(self, quality: str):
        return to_base_quality(quality) in self.qualities


class Chord:
    def __init__(self, chord_text):
        self.name = chord_text

        parser = ChordParser()
        self.__chord_data = parser.parse(chord_text)
        self.__root = Tone(self.__chord_data.root_text)
        self.__bass = Tone(self.__chord_data.bass_text)
        self.__quality = Quality(self.__chord_data.quality_text)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return "<Chord: {}>".format(self.name)

    def __eq__(self, other: Chord) -> bool:
        if not isinstance(other, Chord):
            raise TypeError("{} オブジェクトとChordオブジェクトを比較できません".format(type(other)))

        note_indexes = {note for note in self.get_notes()}
        other_note_indexes = {note for note in self.get_notes()}
        return note_indexes == other_note_indexes

    def __ne__(self, other: Chord) -> bool:
        return not self.__eq__(other)

    @property
    def root(self) -> Tone:
        """
        ルート音を取得します。
        """
        return self.__root

    @property
    def bass(self) -> Tone:
        """
        ベース音を取得します。
        """
        return self.__bass

    @property
    def quality(self) -> Quality:
        """
        コードクオリティを取得します。
        """
        return self.__quality

    @property
    def is_on_chord(self) -> bool:
        """
        オンコードかどうかを取得します。
        """
        return self.root.get_interval() != self.bass.get_interval()

    def get_components(self) -> List[Tone]:
        """
        構成音を取得します。
        """
        components = [self.root, self.root.transpose(4).modified(self.root), self.root.transpose(7).modified(self.root)]
        components_interval = [tone.get_interval_from(self.root) for tone in components]

        chord_tones = self.quality.tones + self.quality.parent_tones
        chord_tones = sorted(chord_tones, key=lambda x: x.base_interval)
        for tone in chord_tones:
            components.append(tone.to_tone(self.root))
            components_interval.append(tone.base_interval + tone.interval_change)

            if tone.delete_interval:
                if tone.delete_interval == DeleteInterval.THIRD and 4 in components_interval:
                    index = components_interval.index(4)
                    components.pop(index)
                    components_interval.pop(index)
                elif tone.delete_interval == DeleteInterval.FIFTH and 7 in components_interval:
                    index = components_interval.index(7)
                    components.pop(index)
                    components_interval.pop(index)


        for base_quality in self.quality.qualities:
            interval_change = base_quality.interval_change
            components[0] = components[0].transpose(interval_change[0])
            if 4 in components_interval:
                index = components_interval.index(4)
                components[index] = components[index].transpose(interval_change[1])
                components_interval[index] = components_interval[index] + interval_change[1]
            if 7 in components_interval:
                index = components_interval.index(7)
                components[index] = components[index].transpose(interval_change[2])
                components_interval[index] = components_interval[index] + interval_change[2]
            if base_quality.type == ChordBaseQualityType.DIMINISHED and 10 in components_interval:
                index = components_interval.index(10)
                components[index] = components[index].transpose(-1)
                components_interval[index] = components_interval[index] - 1

        components, components_interval = zip(*sorted(zip(components, components_interval), key=lambda x: x[1]))

        if self.is_on_chord:
            components = [self.bass,] + list(components)
            components_interval = [0,] + [
                interval - self.bass.get_interval() if self.bass.get_interval() < interval
                else self.bass.get_interval() - interval
                for interval in list(components_interval)]
        return list(components), list(components_interval)

    def get_notes(self, sparse=False) -> List[Tone]:
        """
        コードの構成音インデックスリストを取得します。
        """
        components, _ = self.get_components()

        if sparse:
            # 非構成音は0
            sparse_notes = [0 for _ in range(12)]

            # 構成音は1
            for tone in components:
                sparse_notes[tone.get_interval()] = 1

            # ベース音は2
            sparse_notes[self.bass.get_interval()] = 2
            notes = sparse_notes
        else:
            notes = [tone.get_interval() for tone in components]

        return notes

    def transpose(self, steps: int) -> Chord:
        """
        転調したコードを返します
        """
        if self.is_on_chord:
            return Chord(self.root.transpose(steps).name +
                         self.quality.name +
                         "/" + self.bass.transpose(steps).name)
        else:
            return Chord(self.root.transpose(steps).name +
                         self.quality.name)

    def modified_accidentals(self, major_key: str | Tone) -> Chord:
        """
        臨時記号を修正します
        """
        if isinstance(major_key, Tone):
            base_tone = major_key
        else:
            base_tone = Tone(major_key)

        scale = get_scale(base_tone, scale=Scale.MAJOR)
        _, intervals = self.get_components()

        modified_bass = self.bass.modified(base_tone)
        if self.bass.get_interval_from(base_tone) == 6:
            # M7ありもしくはm無し
            if 11 in intervals or 3 not in intervals:
                modified_bass = scale[7].transpose(-1)

        if self.is_on_chord:
            modified_root = self.root.modified(base_tone)
            root_chord = Chord(modified_root.name + self.quality.name)
            root_chord_components, _ = root_chord.get_components()
            root_chord_intervals = [tone.get_interval() for tone in root_chord_components]
            # ルートコードにベースが含まれる場合、ルートコードの構成音を利用する
            if modified_bass.get_interval() in root_chord_intervals:
                index = root_chord_intervals.index(modified_bass.get_interval())
                modified_bass = root_chord_components[index]
            else:
                modified_root = modified_root.modified(modified_bass)
            return Chord(modified_root.name + self.quality.name + "/" + modified_bass.name)
        else:
            return Chord(modified_bass.name + self.quality.name)


    def reconfigured(self) -> Chord:
        """
        コードを再構成します。
        """

        rec_chord = interval_to_chords(self.get_notes())[0]
        return rec_chord.modified_accidentals(rec_chord.root)


def __chord_sort_func(chord: Chord) -> int:
    eval_score = 0

    relative_bass = chord.root.transpose(chord.bass.get_interval_from(chord.root))
    add_tones = [tone.to_tone(chord.root) for tone in chord.quality.add_tones]
    if relative_bass in add_tones:
        eval_score -= 1

    tones = [tone.to_tone(chord.root) for tone in chord.quality.tones + chord.quality.parent_tones]
    if chord.is_on_chord:
        eval_score -= 1

        if ChordTone.create_from_name("11").to_tone(chord.root) in add_tones:
            eval_score -= 1

        if "sus" in chord.quality.qualities: # 修正必要
            eval_score -= 1

            if ChordTone.create_from_name("9").to_tone(chord.root) in tones:
                eval_score -= 1

        if ChordTone.create_from_name("5").to_tone(chord.root) in tones:
            eval_score -= 2

        if "7(b13)" == chord.quality.name:
            eval_score -= 1

    seventh_note = ChordTone.create_from_name("7").to_tone(chord.root)
    if relative_bass == seventh_note:
        if seventh_note in tones:
            eval_score += 1

            if chord.quality.exists("aug"):
                eval_score -= 1

    return eval_score


def __match_quality(notes: List[int], omit_five_note: bool=False, omit_third_note: bool=False) -> List[str]:
    """
    ノートのリストから一致するクオリティを検索します。
    """
    relative_notes = []
    for i in range(len(notes)):
        relative_notes.append((notes[i] - notes[0]) % 12)

    relative_notes = set(relative_notes)

    for quality_name, notes_origin in const.CHORD_MAP.items():
        notes_origin = set(notes_origin)
        if relative_notes == notes_origin:
            return True, quality_name

        omitted_notes = relative_notes.copy()
        # 5度の音を省略して検索
        if omit_five_note:
            five_note_index = 7
            if five_note_index in omitted_notes:
                omitted_notes.remove(five_note_index)
            if five_note_index in notes_origin:
                notes_origin.remove(five_note_index)

            if omitted_notes == notes_origin:
                return True, quality_name

        # 3度の音を省略して検索
        if omit_third_note:
            third_note_index = 4
            if third_note_index in omitted_notes:
                omitted_notes.remove(third_note_index)
            if third_note_index in notes_origin:
                notes_origin.remove(third_note_index)

            if omitted_notes == notes_origin:
                return True, quality_name

    return False, ""

def tone_to_chords(tones: List[Tone]) -> List[Chord]:
    return interval_to_chords([tone.get_interval() for tone in tones])

def interval_to_chords(intervals: List[int], sort_func=__chord_sort_func) -> List[Chord]:
    """
    ノーツリストから該当するコードの候補のリストを取得します。
    """

    # 重複ノーツは不要
    intervals = sorted(set(intervals), key=intervals.index)

    shifted_notes = intervals[1:]

    chord_list = []
    bass_note = intervals[0]
    # ベースを含まない転回系
    for i in range(len(shifted_notes)):
        is_match, quality = __match_quality(shifted_notes)
        if is_match:
            root_note = shifted_notes[0]

            on_chord = ""
            if bass_note != root_note:
                on_chord = "/" + Tone.create_from_interval(bass_note).to_flat_scale().name

            chord = Chord(Tone.create_from_interval(root_note).to_flat_scale().name + quality + on_chord)
            chord_list.append(chord)

        note = shifted_notes.pop(0)
        shifted_notes.append(note)

    # ベースを含む転回系
    shifted_notes.insert(0, bass_note)
    for i in range(len(shifted_notes)):
        is_match, quality = __match_quality(shifted_notes)
        if is_match:
            root_note = shifted_notes[0]

            on_chord = ""
            if bass_note != root_note:
                on_chord = "/" + Tone.create_from_interval(bass_note).to_flat_scale().name

            chord = Chord(Tone.create_from_interval(root_note).to_flat_scale().name + quality + on_chord)
            chord_list.append(chord)

        note = shifted_notes.pop(0)
        shifted_notes.append(note)

    chord_list = sorted(chord_list, key=sort_func, reverse=True)
    return chord_list

if __name__ == '__main__':
    scale = get_scale(base_tone=Tone("C"), scale=Scale.MINOR)
    for s in scale:
        print(s)

    for chord_tone in chord_tone_list:
        print(chord_tone.name, chord_tone.to_tone(Tone("B#")))

    print(Quality("m7(9)"))
