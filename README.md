# DL-Chordx

[![PyPI](https://img.shields.io/pypi/v/dlchordx.svg)](https://pypi.org/project/dlchordx)

## 概要

和音を解析するライブラリ。

以下のようなことができます。

- 構成音の解析
- 移調
- 構成音からコード検索

## インストール

```sh
$ pip install dlchordx
```

## コード作成

```python
>>> from dlchordx import Chord
>>> chord = Chord("C")
>>> chord
<Chord: C>
```

## コード検索

```python
>>> from dlchordx import interval_to_chords, Tone
>>> chords = tone_to_chords([Tone("C"), Tone("E"), Tone("G")])
>>> chords
[<Chord : C>]

>>> chords = tone_to_chords([Tone("B"), Tone("Db"), Tone("F"), Tone("A")])
>>> chords
[<Chord: Faug/B>, <Chord: Dbaug/B>, <Chord: Aaug/B>]
```

## ルート音取得

```python
>>> from dlchordx import Chord
>>> chord = Chord("C")
>>> print(chord.root)
<Tone: C>

>>> from dlchordx import Chord
>>> chord = Chord("C/G")
>>> print(chord.root)
<Tone: C>

```

## ベース音取得

```python
>>> from dlchordx import Chord
>>> chord = Chord("C")
>>> print(chord.bass)
<Tone: C>

>>> from dlchordx import Chord
>>> chord = Chord("C/G")
>>> print(chord.bass)
<Tone: G>

```

## 移調

```python
>>> from dlchordx import Chord
>>> chord = Chord("C")
>>> t_chord = chord.transpose(steps=1)
>>> t_chord
<Chord: C#>
```

## 臨時記号修正

```python
>>> from dlchordx import Chord
>>> chord = Chord("E/Ab")
>>> chord.modified_accidentals("C")
E/G#

>>> chord = Chord("C#7")
>>> chord.modified_accidentals("C")
Db7
```

## コード最適化

```python
>>> from dlchordx import Chord
>>> chord = Chord("E/Ab")
>>> chord.reconfigured()
E/G#

>>> chord = Chord("AM7/F#")
>>> chord.reconfigured()
F#m7(9)
```

## 構成音取得(インデックス)

```python
>>> from dlchordx import Chord
>>> chord = Chord("C")
>>> cons = chord.get_notes(sparse=False)
>>> print(cons)
[0 4 7]

>>> cons = chord.get_notes(sparse=True)
>>> print(cons)
[2. 0. 0. 0. 1. 0. 0. 1. 0. 0. 0. 0.]
# ベース音 2
# 構成音 1
# 非構成音 0
```

## 構成音取得

```python
>>> from dlchordx import Chord
>>> chord = Chord("C")
>>> components, intervals = chord.get_components()
>>> print(components, intervals)
[<Tone: C>, <Tone: E>, <Tone: G>] [0, 4, 7]

```

## コードを比較

```python
>>> from dlchordx import Chord
>>> Chord("C") == Chord("C")
True
>>> Chord("C") == Chord("C7")
False
>>> Chord("C#") == Chord("Db")
True
>>> Chord("F/D") == Chord("Dm7")
True
>>> Chord("C#dim7/A") == Chord("A7(b9)")
True
```

## コード進行に基づく臨時記号の修正

```python
>>> from dlchordx import ChordProg, Chord
>>> prog = ChordProg([Chord("E7"), Chord("Abdim7"), Chord("Gm7")], major_key="C")
>>> print(prog.modified_accidentals())
[<Chord: E7>, <Chord: G#dim7>, <Chord: Am7>]
```
