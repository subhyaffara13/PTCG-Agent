
def test_XXM_str():

    A = DomainMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], (3, 3), ZZ)

    assert str(A) == \
        'DomainMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], (3, 3), ZZ)'
    assert str(A.to_ddm()) == \
        '[[1, 2, 3], [4, 5, 6], [7, 8, 9]]'
    assert str(A.to_sdm()) == \
        '{0: {0: 1, 1: 2, 2: 3}, 1: {0: 4, 1: 5, 2: 6}, 2: {0: 7, 1: 8, 2: 9}}'

    assert repr(A) == \
        'DomainMatrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], (3, 3), ZZ)'
    assert repr(A.to_ddm()) == \
        'DDM([[1, 2, 3], [4, 5, 6], [7, 8, 9]], (3, 3), ZZ)'
    assert repr(A.to_sdm()) == \
        'SDM({0: {0: 1, 1: 2, 2: 3}, 1: {0: 4, 1: 5, 2: 6}, 2: {0: 7, 1: 8, 2: 9}}, (3, 3), ZZ)'

    B = DomainMatrix({0: {0: ZZ(1), 1: ZZ(2)}, 1: {0: ZZ(3)}}, (2, 2), ZZ)

    assert str(B) == \
        'DomainMatrix({0: {0: 1, 1: 2}, 1: {0: 3}}, (2, 2), ZZ)'
    assert str(B.to_ddm()) == \
        '[[1, 2], [3, 0]]'
    assert str(B.to_sdm()) == \
        '{0: {0: 1, 1: 2}, 1: {0: 3}}'

    assert repr(B) == \
        'DomainMatrix({0: {0: 1, 1: 2}, 1: {0: 3}}, (2, 2), ZZ)'

    if GROUND_TYPES != 'gmpy':
        assert repr(B.to_ddm()) == \
            'DDM([[1, 2], [3, 0]], (2, 2), ZZ)'
        assert repr(B.to_sdm()) == \
            'SDM({0: {0: 1, 1: 2}, 1: {0: 3}}, (2, 2), ZZ)'
    else:
        assert repr(B.to_ddm()) == \
            'DDM([[mpz(1), mpz(2)], [mpz(3), mpz(0)]], (2, 2), ZZ)'
        assert repr(B.to_sdm()) == \
            'SDM({0: {0: mpz(1), 1: mpz(2)}, 1: {0: mpz(3)}}, (2, 2), ZZ)'

    if GROUND_TYPES == 'flint':

        assert str(A.to_dfm()) == \
            '[[1, 2, 3], [4, 5, 6], [7, 8, 9]]'
        assert str(B.to_dfm()) == \
            '[[1, 2], [3, 0]]'

        assert repr(A.to_dfm()) == \
            'DFM([[1, 2, 3], [4, 5, 6], [7, 8, 9]], (3, 3), ZZ)'
        assert repr(B.to_dfm()) == \
            'DFM([[1, 2], [3, 0]], (2, 2), ZZ)'

