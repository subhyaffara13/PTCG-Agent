
def test_bf_pell():
    assert diop_bf_DN(13, -4) == [(3, 1), (-3, 1), (36, 10)]
    assert diop_bf_DN(13, 27) == [(12, 3), (-12, 3), (40, 11), (-40, 11)]
    assert diop_bf_DN(167, -2) == []
    assert diop_bf_DN(1729, 1) == [(44611924489705, 1072885712316)]
    assert diop_bf_DN(89, -8) == [(9, 1), (-9, 1)]
    assert diop_bf_DN(21257, -1) == [(13913102721304, 95427381109)]
    assert diop_bf_DN(340, -4) == [(756, 41)]
    assert diop_bf_DN(-1, 0, t) == [(0, 0)]
    assert diop_bf_DN(0, 0, t) == [(0, t)]
    assert diop_bf_DN(4, 0, t) == [(2*t, t), (-2*t, t)]
    assert diop_bf_DN(3, 0, t) == [(0, 0)]
    assert diop_bf_DN(1, -2, t) == []

