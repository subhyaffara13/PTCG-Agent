
def test_get_type_hints(name: type, tup: TypeTup) -> None:
    """Test `typing.get_type_hints`."""
    typ = tup.typ

    def func(a: typ) -> None: pass

    out = get_type_hints(func)
    ref = {"a": typ, "return": type(None)}
    assert out == ref

