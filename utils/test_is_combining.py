
def test_is_combining():
    line = "v̇_m"
    assert [is_combining(sym) for sym in line] == \
        [False, True, False, False]

