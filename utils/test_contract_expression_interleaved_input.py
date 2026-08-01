
def test_contract_expression_interleaved_input() -> None:
    x, y, z = (np.random.randn(2, 2) for _ in "xyz")
    expected = np.einsum(x, [0, 1], y, [1, 2], z, [2, 3], [3, 0])
    xshp, yshp, zshp = ((2, 2) for _ in "xyz")
    expr = contract_expression(xshp, [0, 1], yshp, [1, 2], zshp, [2, 3], [3, 0])
    out = expr(x, y, z)
    assert np.allclose(out, expected)

