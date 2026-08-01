
def test_infinite_symbol_inequalities():
    x = Symbol('x', extended_positive=True, infinite=True)
    y = Symbol('y', extended_positive=True, infinite=True)
    z = Symbol('z', extended_negative=True, infinite=True)
    w = Symbol('w', extended_negative=True, infinite=True)

    inf_set = (x, y, oo)
    ninf_set = (z, w, -oo)

    for inf1 in inf_set:
        assert (inf1 < 1) is S.false
        assert (inf1 > 1) is S.true
        assert (inf1 <= 1) is S.false
        assert (inf1 >= 1) is S.true

        for inf2 in inf_set:
            assert (inf1 < inf2) is S.false
            assert (inf1 > inf2) is S.false
            assert (inf1 <= inf2) is S.true
            assert (inf1 >= inf2) is S.true

        for ninf1 in ninf_set:
            assert (inf1 < ninf1) is S.false
            assert (inf1 > ninf1) is S.true
            assert (inf1 <= ninf1) is S.false
            assert (inf1 >= ninf1) is S.true
            assert (ninf1 < inf1) is S.true
            assert (ninf1 > inf1) is S.false
            assert (ninf1 <= inf1) is S.true
            assert (ninf1 >= inf1) is S.false

    for ninf1 in ninf_set:
        assert (ninf1 < 1) is S.true
        assert (ninf1 > 1) is S.false
        assert (ninf1 <= 1) is S.true
        assert (ninf1 >= 1) is S.false

        for ninf2 in ninf_set:
            assert (ninf1 < ninf2) is S.false
            assert (ninf1 > ninf2) is S.false
            assert (ninf1 <= ninf2) is S.true
            assert (ninf1 >= ninf2) is S.true

