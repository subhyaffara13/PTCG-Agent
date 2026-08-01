
def test_necklaces():
    def count(n, k, f):
        return len(list(necklaces(n, k, f)))
    m = []
    for i in range(1, 8):
        m.append((
        i, count(i, 2, 0), count(i, 2, 1), count(i, 3, 1)))
    assert Matrix(m) == Matrix([
        [1,   2,   2,   3],
        [2,   3,   3,   6],
        [3,   4,   4,  10],
        [4,   6,   6,  21],
        [5,   8,   8,  39],
        [6,  14,  13,  92],
        [7,  20,  18, 198]])

