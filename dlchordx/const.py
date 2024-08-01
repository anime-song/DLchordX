from collections import OrderedDict

CHORD_MAP = OrderedDict((
    # 2 notes
    ('5', (0, 7)),
    # 3 notes
    ('', (0, 4, 7)),
    ('m', (0, 3, 7)),
    ('dim', (0, 3, 6)),
    ('aug', (0, 4, 8)),
    ('sus2', (0, 2, 7)),
    ('sus4', (0, 5, 7)),
    # 4 notes
    ('6', (0, 4, 7, 9)),
    ('7', (0, 4, 7, 10)),
    ('M7', (0, 4, 7, 11)),
    ('m6', (0, 3, 7, 9)),
    ('m7', (0, 3, 7, 10)),
    ('mM7', (0, 3, 7, 11)),
    ('7-5', (0, 4, 6, 10)),
    ('M7-5', (0, 4, 6, 11)),
    ('m7-5', (0, 3, 6, 10)),
    ('aug7', (0, 4, 8, 10)),
    ('augM7', (0, 4, 8, 11)),
    ('aug(b9)', (0, 4, 8, 1)),
    ('7sus4', (0, 5, 7, 10)),
    ('dim7', (0, 3, 6, 9)),
    ('add9', (0, 4, 7, 2)),
    ('add11', (0, 4, 7, 5)),
    ('madd9', (0, 3, 7, 2)),

    # 5 notes
    ('69', (0, 4, 7, 9, 2)),
    ('7(9)', (0, 4, 7, 10, 2)),
    ('7(13)', (0, 4, 7, 10, 9)),
    ('7(b9)', (0, 4, 7, 10, 1)),
    ('7(#9)', (0, 4, 7, 10, 3)),
    ('7(#11)', (0, 4, 7, 10, 6)),
    ('7(b13)', (0, 4, 7, 10, 8)),
    ('7-5(9)', (0, 4, 6, 10, 2)),
    ('7-5(#9)', (0, 4, 6, 10, 3)),
    ('7-5(b13)', (0, 4, 6, 10, 8)),
    ('7sus4(9)', (0, 5, 7, 10, 2)),
    ('7sus4(b9)', (0, 5, 7, 10, 1)),
    ('M7(9)', (0, 4, 7, 11, 2)),
    ('M7(13)', (0, 4, 7, 11, 9)),
    ('M7(#11)', (0, 4, 7, 11, 6)),
    ('M7(b9)', (0, 4, 7, 11, 1)),
    ('m69', (0, 3, 7, 9, 2)),
    ('m7(9)', (0, 3, 7, 10, 2)),
    ('m7(11)', (0, 3, 7, 10, 5)),
    ('m7(13)', (0, 3, 7, 10, 9)),
    ('m7(b9)', (0, 3, 7, 10, 1)),
    ('m7-5(11)', (0, 3, 6, 10, 5)),
    ('mM7(9)', (0, 3, 7, 11, 2)),
    ('mM7(13)', (0, 3, 7, 11, 9)),
    ('aug7(9)', (0, 4, 8, 10, 2)),
    ('augM7(#9)', (0, 4, 8, 11, 3)),

    # 6 notes
    ('7(9, 11)', (0, 4, 7, 10, 2, 5)),
    ('7(9, 13)', (0, 4, 7, 10, 2, 9)),
    ('7(9, b13)', (0, 4, 7, 10, 2, 8)),
    ('7(9, #11)', (0, 4, 7, 10, 2, 6)),
    ('7(b9, 13)', (0, 4, 7, 10, 1, 9)),
    ('7(b9, b13)', (0, 4, 7, 10, 1, 8)),
    ('7(b9, #9)', (0, 4, 7, 10, 1, 3)),
    ('7(b9, #11)', (0, 4, 7, 10, 1, 6)),
    ('7(#9, 13)', (0, 4, 7, 10, 3, 9)),
    ('7(#9, b13)', (0, 4, 7, 10, 3, 8)),
    ('7(#9, #11)', (0, 4, 7, 10, 3, 6)),
    ('7(#11, 13)', (0, 4, 7, 10, 6, 9)),
    ('m7(9, 11)', (0, 3, 7, 10, 2, 5)),
    ('m7(9, 13)', (0, 3, 7, 10, 2, 9)),
    ('M7(9, 11)', (0, 4, 7, 11, 2, 5)),
    ('M7(9, 13)', (0, 4, 7, 11, 2, 9)),
    ('M7(9, #11)', (0, 4, 7, 11, 2, 6)),

    # 7 notes
    ('7(9, 11, 13)', (0, 4, 7, 10, 2, 5, 9)),
    ('7(9, #11, 13)', (0, 4, 7, 10, 2, 6, 9)),
    ('7(9, #11, b13)', (0, 4, 7, 10, 2, 6, 8)),
    ('7(b9, #11, 13)', (0, 4, 7, 10, 1, 6, 9)),
    ('m7(9, 11, 13)', (0, 3, 7, 10, 2, 5, 9)),
    ('M7(9, 11, 13)', (0, 4, 7, 11, 2, 5, 9)),
    ('M7(9, #11, 13)', (0, 4, 7, 11, 2, 6, 9)),

))
