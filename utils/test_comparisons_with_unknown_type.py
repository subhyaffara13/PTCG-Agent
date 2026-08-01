
def test_comparisons_with_unknown_type():
    class Foo:
        """
        Class that is unaware of Basic, and relies on both classes returning
        the NotImplemented singleton for equivalence to evaluate to False.

        """

    ni, nf, nr = Integer(3), Float(1.0), Rational(1, 3)
    foo = Foo()

    for n in ni, nf, nr, oo, -oo, zoo, nan:
        assert n != foo
        assert foo != n
        assert not n == foo
        assert not foo == n
        raises(TypeError, lambda: n < foo)
        raises(TypeError, lambda: foo > n)
        raises(TypeError, lambda: n > foo)
        raises(TypeError, lambda: foo < n)
        raises(TypeError, lambda: n <= foo)
        raises(TypeError, lambda: foo >= n)
        raises(TypeError, lambda: n >= foo)
        raises(TypeError, lambda: foo <= n)

    class Bar:
        """
        Class that considers itself equal to any instance of Number except
        infinities and nans, and relies on SymPy types returning the
        NotImplemented singleton for symmetric equality relations.

        """
        def __eq__(self, other):
            if other in (oo, -oo, zoo, nan):
                return False
            if isinstance(other, Number):
                return True
            return NotImplemented

        def __ne__(self, other):
            return not self == other

    bar = Bar()

    for n in ni, nf, nr:
        assert n == bar
        assert bar == n
        assert not n != bar
        assert not bar != n

    for n in oo, -oo, zoo, nan:
        assert n != bar
        assert bar != n
        assert not n == bar
        assert not bar == n

    for n in ni, nf, nr, oo, -oo, zoo, nan:
        raises(TypeError, lambda: n < bar)
        raises(TypeError, lambda: bar > n)
        raises(TypeError, lambda: n > bar)
        raises(TypeError, lambda: bar < n)
        raises(TypeError, lambda: n <= bar)
        raises(TypeError, lambda: bar >= n)
        raises(TypeError, lambda: n >= bar)
        raises(TypeError, lambda: bar <= n)

