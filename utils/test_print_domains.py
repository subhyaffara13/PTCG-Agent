
def test_print_domains():
    from sympy.sets import Integers, Naturals, Naturals0, Reals, Complexes

    assert mpp.doprint(Complexes) == '<mi mathvariant="normal">&#x2102;</mi>'
    assert mpp.doprint(Integers) == '<mi mathvariant="normal">&#x2124;</mi>'
    assert mpp.doprint(Naturals) == '<mi mathvariant="normal">&#x2115;</mi>'
    assert mpp.doprint(Naturals0) == \
        '<msub><mi mathvariant="normal">&#x2115;</mi><mn>0</mn></msub>'
    assert mpp.doprint(Reals) == '<mi mathvariant="normal">&#x211D;</mi>'

