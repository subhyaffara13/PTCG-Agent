
def test_f1a2():
    #issue 3509:
    assert limit(((x - 1)/(x + 1))**x, x, oo) == exp(-2)  # Primer 9

