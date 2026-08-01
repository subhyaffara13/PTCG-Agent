
def test_complex_indices():
    i, j = symbols('i j', integer=True)
    A = Indexed('A', i, i + j)
    assert A.rank == 2
    assert A.indices == (i, i + j)

