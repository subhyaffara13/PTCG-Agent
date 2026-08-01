
def test_none(doc):
    assert doc(m.get_none) == "get_none() -> None"
    assert doc(m.print_none) == "print_none(arg0: None) -> None"


def test_none(value: t.Any) -> bool:
    """Return true if the variable is none."""
    return value is None


def test_none():
    assert none.is_Atom
    assert none == none
    class Foo(Token):
        pass
    foo = Foo()
    assert foo != none
    assert none == None
    assert none == NoneToken()
    assert none.func(*none.args) == none

