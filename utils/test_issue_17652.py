
def test_issue_17652():
    """Regression test issue #17652.

    IndexedBase.label should not upcast subclasses of Symbol
    """
    class SubClass(Symbol):
        pass

    x = SubClass('X')
    assert type(x) == SubClass
    base = IndexedBase(x)
    assert type(x) == SubClass
    assert type(base.label) == SubClass

