
def test_failing_assumptions():
    x = Symbol('x', positive=True)
    y = Symbol('y')
    assert failing_assumptions(6*x + y, **x.assumptions0) == \
    {'real': None, 'imaginary': None, 'complex': None, 'hermitian': None,
    'positive': None, 'nonpositive': None, 'nonnegative': None, 'nonzero': None,
    'negative': None, 'zero': None, 'extended_real': None, 'finite': None,
    'infinite': None, 'extended_negative': None, 'extended_nonnegative': None,
    'extended_nonpositive': None, 'extended_nonzero': None,
    'extended_positive': None }

