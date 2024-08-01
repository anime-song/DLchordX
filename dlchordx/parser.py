import re
from typing import List

class ChordParseData(object):
    def __init__(self, root_text, bass_text, quality_text):
        self.__root_text = root_text
        self.__bass_text = bass_text
        self.__quality_text = quality_text

    @property
    def root_text(self):
        return self.__root_text

    @property
    def bass_text(self):
        return self.__bass_text

    @property
    def quality_text(self):
        return self.__quality_text


class ChordParser(object):
    """
    コードをルート、クオリティ、ベースに分解するクラス。
    """

    def parse(self, chord_text: str) -> ChordParseData:
        split_text = chord_text.split("/")
        root_text = chord_text[0]
        bass_text = ""
        accidentals_text = ""

        if len(split_text) > 1:
            bass_text = split_text[1]

        res = split_text[0][1:]
        for i in range(len(res)):
            if res[i] != "#" and res[i] != "b":
                break
            accidentals_text += res[i]

        root_text += accidentals_text
        quality_text = res[len(accidentals_text):]

        # ベースがない場合はルート音がベースになります
        if bass_text == "":
            bass_text = root_text

        return ChordParseData(root_text, bass_text, quality_text)



class QualityParseData(object):
    def __init__(self, qualities, tones, tones_parentheses):
        self.__qualities = qualities
        self.__tones = tones
        self.__tones_parentheses = tones_parentheses

    @property
    def qualities(self):
        """
        クオリティ部分のみのテキストリストを取得します。
        :return: クオリティのテキストリスト
        :rtype: list[str]
        """
        return self.__qualities

    @property
    def tones(self):
        """
        括弧外の構成音のリストを取得します。
        :return: 括弧外の構成音のリスト
        :rtype: list[str]
        """
        return self.__tones

    @property
    def tones_parentheses(self):
        """
        括弧内の構成音のリストを取得します。
        :return: 括弧内の構成音のリスト
        :rtype: list[str]
        """
        return self.__tones_parentheses


class QualityParser(object):
    def __init__(self) -> None:
        self.__tone_list = ["5", "6", "-5", "b5", "+5", "#5", "-9", "b9", "9", "+9", "#9", "+11", "#11", "11", "-13", "b13", "13"]
    """
    コードクオリティを解析するクラス
    """

    def __find_tone_parentheses(self, quality_text: str) -> List[str]:
        """
        括弧内の構成音を探します。
        :param quality_text: コードクオリティのテキスト
        :type quality_text: str
        :return: 括弧内の構成音のリスト
        :rtype: list[str]
        """
        match = re.search(r"(\()(.*?)(\))", quality_text)
        if match is None:
            return []

        if len(match.groups()) < 3:
            return []

        tone_raw_text = match.group(2)
        tones_text = tone_raw_text.split(",")
        tones = []

        for tone_text in tones_text:
            tone = tone_text.strip()

            if tone not in self.__tone_list:
                raise ValueError("括弧内の構成音 {} が不明です".format(tone))

            tones.append(tone)
        return tones

    def __find_tone(self, quality_text: str) -> List[str]:
        """
        括弧外の構成音を探します。
        :param quality_text: コードクオリティのテキスト
        :type quality_text: str
        :return: 括弧外の構成音のリスト
        :rtype: list[str]
        """
        exclude_parentheses = re.sub(r"(\()(.*?)(\))", "", quality_text)

        tones = []
        if "add" in exclude_parentheses:
            match = re.findall(r"add9|add11|add4|add2", exclude_parentheses)
            exclude_parentheses = re.sub(r"add9|add11|add4|add2", "", exclude_parentheses)
            for tone in match:
                tones.append(tone)

        if "sus" in exclude_parentheses:
            match = re.findall(r"sus2|sus4", exclude_parentheses)
            exclude_parentheses = re.sub(r"sus2|sus4", "", exclude_parentheses)
            for tone in match:
                tones.append(tone)

        match_tones = re.findall("9|11|13|[-+b#]5|2|4|6|(?<![-+b#])5", exclude_parentheses)

        for tone in match_tones:
            if tone not in self.__tone_list:
                raise ValueError("括弧外の構成音 {} が不明です".format(tone))

        match_tones.extend(tones)
        return match_tones

    def __find_base_quality(self, quality_text: str) -> List[str]:
        """
        ベースクオリティを取得します。
        :param quality_text: コードクオリティのテキスト
        :type quality_text: str
        :return: クオリティのリスト
        :rtype: list[str]
        """
        qualities = []
        match = re.findall(r"aug|dim", quality_text)
        if match:
            qualities.extend(match)
            quality_text = re.sub(r"aug|dim", "", quality_text)

        match = re.findall(r"m", quality_text)
        if match:
            qualities.extend(match)
            quality_text = re.sub(r"m", "", quality_text)

        return qualities

    def __get_add_tones(self, quality_text: str, tones: List[str]) -> List[str]:
        add_tones = []
        if "7" in quality_text:
            add_tones.append("7")

        for tension in tones:
            if tension == "13":
                add_tones.extend(["7", "9", "11"])
            elif tension == "11":
                add_tones.extend(["7", "9"])
            elif tension == "9" and "6" not in tones:
                add_tones.extend(["7"])

        if "M" in quality_text:
            add_tones.remove("7")
            add_tones.append("M7")

        return list(set(add_tones))

    def parse(self, quality_text: str) -> QualityParseData:
        tones_parentheses = self.__find_tone_parentheses(quality_text)
        tones = self.__find_tone(quality_text)
        qualities = self.__find_base_quality(quality_text)

        add_tones = self.__get_add_tones(quality_text, tones)
        tones.extend(add_tones)

        quality_data = QualityParseData(qualities, tones, tones_parentheses)
        return quality_data

if __name__ == "__main__":
    parser = QualityParser()
    parse_data = parser.parse("M13(#11)")
    print(parse_data.tones_parentheses, parse_data.qualities, parse_data.tones)
