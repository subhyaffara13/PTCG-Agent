
def test_NamedArgsMixin():
    class Foo(Basic, NamedArgsMixin):
        _argnames = 'foo', 'bar'

    a = Foo(S(1), S(2))

    assert a.foo == 1
    assert a.bar == 2

    raises(AttributeError, lambda: a.baz)

    class Bar(Basic, NamedArgsMixin):
        pass

    raises(AttributeError, lambda: Bar(S(1), S(2)).foo)

