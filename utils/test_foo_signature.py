
def test_foo_signature():
    assert str(inspect.signature(Foo.baz)) == "(self, bar=None, *, foobar=None)"

