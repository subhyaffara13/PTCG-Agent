
def test_represent_spin_operators():
    assert represent(Jx) == hbar*Matrix([[0, 1], [1, 0]])/2
    assert represent(
        Jx, j=1) == hbar*sqrt(2)*Matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])/2
    assert represent(Jy) == hbar*I*Matrix([[0, -1], [1, 0]])/2
    assert represent(Jy, j=1) == hbar*I*sqrt(2)*Matrix([[0, -1, 0], [1,
                     0, -1], [0, 1, 0]])/2
    assert represent(Jz) == hbar*Matrix([[1, 0], [0, -1]])/2
    assert represent(
        Jz, j=1) == hbar*Matrix([[1, 0, 0], [0, 0, 0], [0, 0, -1]])

