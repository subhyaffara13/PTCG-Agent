
def test_curry_doesnot_transmogrify():
    # Early versions of `curry` transmogrified to `partial` objects if
    # only one positional argument remained even if keyword arguments
    # were present.  Now, `curry` should always remain `curry`.
    def f(x, y=0):
        return x + y

    cf = curry(f)
    assert cf(y=1)(y=2)(y=3)(1) == f(1, 3)

