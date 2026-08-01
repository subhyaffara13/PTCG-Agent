
def test_minsolve_linear_system():
    pqt = {"quick": True, "particular": True}
    pqf = {"quick": False, "particular": True}
    assert solve([x + y - 5, 2*x - y - 1], **pqt) == {x: 2, y: 3}
    assert solve([x + y - 5, 2*x - y - 1], **pqf) == {x: 2, y: 3}
    def count(dic):
        return len([x for x in dic.values() if x == 0])
    assert count(solve([x + y + z, y + z + a + t], **pqt)) == 3
    assert count(solve([x + y + z, y + z + a + t], **pqf)) == 3
    assert count(solve([x + y + z, y + z + a], **pqt)) == 1
    assert count(solve([x + y + z, y + z + a], **pqf)) == 2
    # issue 22718
    A = Matrix([
        [ 1,  1,  1,  0,  1,  1,  0,  1,  0,  0,  1,  1,  1,  0],
        [ 1,  1,  0,  1,  1,  0,  1,  0,  1,  0, -1, -1,  0,  0],
        [-1, -1,  0,  0, -1,  0,  0,  0,  0,  0,  1,  1,  0,  1],
        [ 1,  0,  1,  1,  0,  1,  1,  0,  0,  1, -1,  0, -1,  0],
        [-1,  0, -1,  0,  0, -1,  0,  0,  0,  0,  1,  0,  1,  1],
        [-1,  0,  0, -1,  0,  0, -1,  0,  0,  0, -1,  0,  0, -1],
        [ 0,  1,  1,  1,  0,  0,  0,  1,  1,  1,  0, -1, -1,  0],
        [ 0, -1, -1,  0,  0,  0,  0, -1,  0,  0,  0,  1,  1,  1],
        [ 0, -1,  0, -1,  0,  0,  0,  0, -1,  0,  0, -1,  0, -1],
        [ 0,  0, -1, -1,  0,  0,  0,  0,  0, -1,  0,  0, -1, -1],
        [ 0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0],
        [ 0,  0,  0,  0, -1, -1,  0, -1,  0,  0,  0,  0,  0,  0]])
    v = Matrix(symbols("v:14", integer=True))
    B = Matrix([[2], [-2], [0], [0], [0], [0], [0], [0], [0],
        [0], [0], [0]])
    eqs = A@v-B
    assert solve(eqs) == []
    assert solve(eqs, particular=True) == []  # assumption violated
    assert all(v for v in solve([x + y + z, y + z + a]).values())
    for _q in (True, False):
        assert not all(v for v in solve(
            [x + y + z, y + z + a], quick=_q,
            particular=True).values())
        # raise error if quick used w/o particular=True
        raises(ValueError, lambda: solve([x + 1], quick=_q))
        raises(ValueError, lambda: solve([x + 1], quick=_q, particular=False))
    # and give a good error message if someone tries to use
    # particular with a single equation
    raises(ValueError, lambda: solve(x + 1, particular=True))

