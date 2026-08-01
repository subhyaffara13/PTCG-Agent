
def test_composite_option():
    assert construct_domain({(1,): sin(y)}, composite=False) == \
        (EX, {(1,): EX(sin(y))})

    assert construct_domain({(1,): y}, composite=False) == \
        (EX, {(1,): EX(y)})

    assert construct_domain({(1, 1): 1}, composite=False) == \
        (ZZ, {(1, 1): 1})

    assert construct_domain({(1, 0): y}, composite=False) == \
        (EX, {(1, 0): EX(y)})

