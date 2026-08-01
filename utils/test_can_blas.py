
def test_can_blas(inp: Any, benchmark: bool) -> None:
    result = blas.can_blas(*inp)
    assert result == benchmark

