
def test_Qubit():
    array = [0, 0, 1, 1, 0]
    qb = Qubit('00110')
    assert qb.flip(0) == Qubit('00111')
    assert qb.flip(1) == Qubit('00100')
    assert qb.flip(4) == Qubit('10110')
    assert qb.qubit_values == (0, 0, 1, 1, 0)
    assert qb.dimension == 5
    for i in range(5):
        assert qb[i] == array[4 - i]
    assert len(qb) == 5
    qb = Qubit('110')

