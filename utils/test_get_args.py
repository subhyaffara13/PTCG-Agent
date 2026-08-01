
def test_get_args(name: type, tup: TypeTup) -> None:
    """Test `typing.get_args`."""
    typ, ref = tup.typ, tup.args
    out = get_args(typ)
    assert out == ref

