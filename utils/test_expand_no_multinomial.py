
def test_expand_no_multinomial():
    assert ((1 + x)*(1 + (1 + x)**4)).expand(multinomial=False) == \
        1 + x + (1 + x)**4 + x*(1 + x)**4

