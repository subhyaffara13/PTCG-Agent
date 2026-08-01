
def test_subclass_deferral(sctype, __op__, __rop__, op, cmp):
    """
    This test covers scalar subclass deferral.  Note that this is exceedingly
    complicated, especially since it tends to fall back to the array paths and
    these additionally add the "array priority" mechanism.

    The behaviour was modified subtly in 1.22 (to make it closer to how Python
    scalars work).  Due to its complexity and the fact that subclassing NumPy
    scalars is probably a bad idea to begin with.  There is probably room
    for adjustments here.
    """
    class myf_simple1(sctype):
        pass

    class myf_simple2(sctype):
        pass

    def op_func(self, other):
        return __op__

    def rop_func(self, other):
        return __rop__

    myf_op = type("myf_op", (sctype,), {__op__: op_func, __rop__: rop_func})

    # inheritance has to override, or this is correctly lost:
    res = op(myf_simple1(1), myf_simple2(2))
    assert type(res) is sctype or type(res) is np.bool
    assert op(myf_simple1(1), myf_simple2(2)) == op(1, 2)  # inherited

    # Two independent subclasses do not really define an order.  This could
    # be attempted, but we do not since Python's `int` does neither:
    assert op(myf_op(1), myf_simple1(2)) == __op__
    assert op(myf_simple1(1), myf_op(2)) == op(1, 2)  # inherited

