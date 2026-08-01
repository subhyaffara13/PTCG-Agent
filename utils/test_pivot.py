
def test_pivot():
    for _ in range(10):
        m = randMatrix(5)
        rref = m.rref()
        for _ in range(5):
            i, j = randint(0, 4), randint(0, 4)
            if m[i, j] != 0:
                assert LRASolver._pivot(m, i, j).rref() == rref

