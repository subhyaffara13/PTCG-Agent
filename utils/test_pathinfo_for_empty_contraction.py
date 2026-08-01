
def test_pathinfo_for_empty_contraction() -> None:
    eq = "->"
    arrays = (1.0,)
    path: PathType = []
    _, info = contract_path(eq, *arrays, optimize=path)
    # some info is built lazily, so check repr
    assert repr(info)
    assert info.largest_intermediate == 1

