
def test_explicit_path() -> None:
    pytest.importorskip("numpy")
    x = oe.contract("a,b,c", [1], [2], [3], optimize=[(1, 2), (0, 1)])
    assert x.item() == 6

