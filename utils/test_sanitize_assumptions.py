
def test_sanitize_assumptions():
    # issue 6666
    for cls in (Symbol, Dummy, Wild):
        x = cls('x', real=1, positive=0)
        assert x.is_real is True
        assert x.is_positive is False
        assert cls('', real=True, positive=None).is_positive is None
        raises(ValueError, lambda: cls('', commutative=None))
    raises(ValueError, lambda: Symbol._sanitize({"commutative": None}))

