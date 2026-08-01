
def test_assumptions_copy():
    assert assumptions(Symbol('x'), {"commutative": True}
        ) == {'commutative': True}
    assert assumptions(Symbol('x'), ['integer']) == {}
    assert assumptions(Symbol('x'), ['commutative']
        ) == {'commutative': True}
    assert assumptions(Symbol('x')) == {'commutative': True}
    assert assumptions(1)['positive']
    assert assumptions(3 + I) == {
        'algebraic': True,
        'commutative': True,
        'complex': True,
        'composite': False,
        'even': False,
        'extended_negative': False,
        'extended_nonnegative': False,
        'extended_nonpositive': False,
        'extended_nonzero': False,
        'extended_positive': False,
        'extended_real': False,
        'finite': True,
        'imaginary': False,
        'infinite': False,
        'integer': False,
        'irrational': False,
        'negative': False,
        'noninteger': False,
        'nonnegative': False,
        'nonpositive': False,
        'nonzero': False,
        'odd': False,
        'positive': False,
        'prime': False,
        'rational': False,
        'real': False,
        'transcendental': False,
        'zero': False}

