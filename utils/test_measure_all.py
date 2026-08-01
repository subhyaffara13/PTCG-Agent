
def test_measure_all():
    assert measure_all(Qubit('11')) == [(Qubit('11'), 1)]
    state = Qubit('11') + Qubit('10')
    assert measure_all(state) == [(Qubit('10'), S.Half),
           (Qubit('11'), S.Half)]
    state2 = Qubit('11')/sqrt(5) + 2*Qubit('00')/sqrt(5)
    assert measure_all(state2) == \
        [(Qubit('00'), Rational(4, 5)), (Qubit('11'), Rational(1, 5))]

    # from issue #12585
    assert measure_all(qapply(Qubit('0'))) == [(Qubit('0'), 1)]

