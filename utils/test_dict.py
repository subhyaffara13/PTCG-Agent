
def test_dict(capture, doc):
    d = m.get_dict()
    assert d == {"key": "value"}

    with capture:
        d["key2"] = "value2"
        m.print_dict(d)
    assert (
        capture.unordered
        == """
        key: key, value=value
        key: key2, value=value2
    """
    )

    assert not m.dict_contains({}, 42)
    assert m.dict_contains({42: None}, 42)
    assert m.dict_contains({"foo": None}, "foo")

    assert doc(m.get_dict) == "get_dict() -> dict"
    assert doc(m.print_dict) == "print_dict(arg0: dict) -> None"

    assert m.dict_keyword_constructor() == {"x": 1, "y": 2, "z": 3}


def test_dict():
    from sympy.abc import x, y, z
    d = {}
    assert srepr(d) == "{}"
    d = {x: y}
    assert srepr(d) == "{Symbol('x'): Symbol('y')}"
    d = {x: y, y: z}
    assert srepr(d) in (
        "{Symbol('x'): Symbol('y'), Symbol('y'): Symbol('z')}",
        "{Symbol('y'): Symbol('z'), Symbol('x'): Symbol('y')}",
    )
    d = {x: {y: z}}
    assert srepr(d) == "{Symbol('x'): {Symbol('y'): Symbol('z')}}"


def test_dict():
    assert str({1: 1 + x}) == sstr({1: 1 + x}) == "{1: x + 1}"
    assert str({1: x**2, 2: y*x}) in ("{1: x**2, 2: x*y}", "{2: x*y, 1: x**2}")
    assert sstr({1: x**2, 2: y*x}) == "{1: x**2, 2: x*y}"

