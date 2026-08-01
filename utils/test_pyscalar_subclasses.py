
def test_pyscalar_subclasses(subtype, __op__, __rop__, op, cmp):
    # This tests that python scalar subclasses behave like a float64 (if they
    # don't override it).
    # In an earlier version of NEP 50, they behaved like the Python builtins.
    def op_func(self, other):
        return __op__

    def rop_func(self, other):
        return __rop__

    # Check that deferring is indicated using `__array_ufunc__`:
    myt = type("myt", (subtype,),
               {__op__: op_func, __rop__: rop_func, "__array_ufunc__": None})

    # Just like normally, we should never presume we can modify the float.
    assert op(myt(1), np.float64(2)) == __op__
    assert op(np.float64(1), myt(2)) == __rop__

    if op in {operator.mod, operator.floordiv} and subtype is complex:
        return  # module is not support for complex.  Do not test.

    if __rop__ == __op__:
        return

    # When no deferring is indicated, subclasses are handled normally.
    myt = type("myt", (subtype,), {__rop__: rop_func})
    behaves_like = lambda x: np.array(subtype(x))[()]

    # Check for float32, as a float subclass float64 may behave differently
    res = op(myt(1), np.float16(2))
    expected = op(behaves_like(1), np.float16(2))
    assert res == expected
    assert type(res) is type(expected)
    res = op(np.float32(2), myt(1))
    expected = op(np.float32(2), behaves_like(1))
    assert res == expected
    assert type(res) is type(expected)
    # Same check for longdouble (compare via dtype to accept float64 when
    # longdouble has the identical size), which is currently not perfectly
    # consistent.
    res = op(myt(1), np.longdouble(2))
    expected = op(behaves_like(1), np.longdouble(2))
    assert res == expected
    assert np.dtype(type(res)) == np.dtype(type(expected))
    res = op(np.float32(2), myt(1))
    expected = op(np.float32(2), behaves_like(1))
    assert res == expected
    assert np.dtype(type(res)) == np.dtype(type(expected))

