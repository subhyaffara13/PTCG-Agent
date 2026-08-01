
def test_args_refcount():
    """Issue/PR #1216 - py::args elements get double-inc_ref()ed when combined with regular
    arguments"""
    refcount = m.arg_refcount_h

    myval = 54321
    expected = refcount(myval)
    assert m.arg_refcount_h(myval) == expected
    assert m.arg_refcount_o(myval) == expected + 1
    assert m.arg_refcount_h(myval) == expected
    assert refcount(myval) == expected

    assert m.mixed_plus_args(1, 2.0, "a", myval) == (1, 2.0, ("a", myval))
    assert refcount(myval) == expected

    assert m.mixed_plus_kwargs(3, 4.0, a=1, b=myval) == (3, 4.0, {"a": 1, "b": myval})
    assert refcount(myval) == expected

    assert m.args_function(-1, myval) == (-1, myval)
    assert refcount(myval) == expected

    assert m.mixed_plus_args_kwargs(5, 6.0, myval, a=myval) == (
        5,
        6.0,
        (myval,),
        {"a": myval},
    )
    assert refcount(myval) == expected

    assert m.args_kwargs_function(7, 8, myval, a=1, b=myval) == (
        (7, 8, myval),
        {"a": 1, "b": myval},
    )
    assert refcount(myval) == expected

    exp3 = refcount(myval, myval, myval)
    assert m.args_refcount(myval, myval, myval) == (exp3, exp3, exp3)
    assert refcount(myval) == expected

    # This function takes the first arg as a `py::object` and the rest as a `py::args`.  Unlike the
    # previous case, when we have both positional and `py::args` we need to construct a new tuple
    # for the `py::args`; in the previous case, we could simply inc_ref and pass on Python's input
    # tuple without having to inc_ref the individual elements, but here we can't, hence the extra
    # refs.
    assert m.mixed_args_refcount(myval, myval, myval) == (exp3 + 3, exp3 + 3, exp3 + 3)

    assert m.class_default_argument() == "<class 'decimal.Decimal'>"

