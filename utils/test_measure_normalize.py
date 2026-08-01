
def test_measure_normalize():
    a, b = symbols('a b')
    state = a*Qubit('110') + b*Qubit('111')
    assert measure_partial(state, (0,), normalize=False) == \
        [(a*Qubit('110'), a*a.conjugate()), (b*Qubit('111'), b*b.conjugate())]
    assert measure_all(state, normalize=False) == \
        [(Qubit('110'), a*a.conjugate()), (Qubit('111'), b*b.conjugate())]

