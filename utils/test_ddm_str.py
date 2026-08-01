
def test_DDM_str():
    ddm = DDM([[ZZ(0), ZZ(1)], [ZZ(2), ZZ(3)]], (2, 2), ZZ)
    if GROUND_TYPES == 'gmpy': # pragma: no cover
        assert str(ddm) == '[[0, 1], [2, 3]]'
        assert repr(ddm) == 'DDM([[mpz(0), mpz(1)], [mpz(2), mpz(3)]], (2, 2), ZZ)'
    else:        # pragma: no cover
        assert repr(ddm) == 'DDM([[0, 1], [2, 3]], (2, 2), ZZ)'
        assert str(ddm) == '[[0, 1], [2, 3]]'


def test_DDM_str():
    sdm = SDM({0:{0:ZZ(1)}, 1:{1:ZZ(1)}}, (2, 2), ZZ)
    assert str(sdm) == '{0: {0: 1}, 1: {1: 1}}'
    if GROUND_TYPES == 'gmpy': # pragma: no cover
        assert repr(sdm) == 'SDM({0: {0: mpz(1)}, 1: {1: mpz(1)}}, (2, 2), ZZ)'
    else:        # pragma: no cover
        assert repr(sdm) == 'SDM({0: {0: 1}, 1: {1: 1}}, (2, 2), ZZ)'

