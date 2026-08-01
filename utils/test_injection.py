
def test_injection():
    parse_maxima('c: x+1', globals=globals())
    # c created by parse_maxima
    assert c == x + 1 # noqa:F821

    parse_maxima('g: sqrt(81)', globals=globals())
    # g created by parse_maxima
    assert g == 9 # noqa:F821

