
def test_common_assumptions():
    assert common_assumptions([0, 1, 2]
        ) == {'algebraic': True, 'irrational': False, 'hermitian':
        True, 'extended_real': True, 'real': True, 'extended_negative':
        False, 'extended_nonnegative': True, 'integer': True,
        'rational': True, 'imaginary': False, 'complex': True,
        'commutative': True,'noninteger': False, 'composite': False,
        'infinite': False, 'nonnegative': True, 'finite': True,
        'transcendental': False,'negative': False}
    assert common_assumptions([0, 1, 2], 'positive integer'.split()
        ) == {'integer': True}
    assert common_assumptions([0, 1, 2], []) == {}
    assert common_assumptions([], ['integer']) == {}
    assert common_assumptions([0], ['integer']) == {'integer': True}

