
def test_orthogonal_states():
    bracket = OrthogonalBra(x) * OrthogonalKet(x)
    assert bracket.doit() == 1

    bracket = OrthogonalBra(x) * OrthogonalKet(x+1)
    assert bracket.doit() == 0

    bracket = OrthogonalBra(x) * OrthogonalKet(y)
    assert bracket.doit() == bracket

