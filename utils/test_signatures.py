
def test_signatures():
    assert m.kw_only_all.__doc__ == "kw_only_all(*, i: int, j: int) -> tuple\n"
    assert m.kw_only_mixed.__doc__ == "kw_only_mixed(i: int, *, j: int) -> tuple\n"
    assert m.pos_only_all.__doc__ == "pos_only_all(i: int, j: int, /) -> tuple\n"
    assert m.pos_only_mix.__doc__ == "pos_only_mix(i: int, /, j: int) -> tuple\n"
    assert (
        m.pos_kw_only_mix.__doc__
        == "pos_kw_only_mix(i: int, /, j: int, *, k: int) -> tuple\n"
    )

