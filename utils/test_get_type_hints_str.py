
def test_get_type_hints_str(name: type, tup: TypeTup) -> None:
    """Test `typing.get_type_hints` with string-representation of types."""
    typ_str, typ = f"npt.{name}", tup.typ

    def func(a: typ_str) -> None: pass

    out = get_type_hints(func)
    ref = {"a": getattr(npt, str(name)), "return": type(None)}
    assert out == ref

