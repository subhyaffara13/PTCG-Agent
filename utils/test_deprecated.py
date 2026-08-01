
def test_deprecated():
    @deprecated('deprecated_function is deprecated',
                deprecated_since_version='1.10',
                # This is the target at the top of the file, which will never
                # go away.
                active_deprecations_target='active-deprecations')
    def deprecated_function(x):
        return x

    with warns_deprecated_sympy():
        assert deprecated_function(1) == 1

    @deprecated('deprecated_class is deprecated',
                deprecated_since_version='1.10',
                active_deprecations_target='active-deprecations')
    class deprecated_class:
        pass

    with warns_deprecated_sympy():
        assert isinstance(deprecated_class(), deprecated_class)

    # Ensure the class decorator works even when the class never returns
    # itself
    @deprecated('deprecated_class_new is deprecated',
                deprecated_since_version='1.10',
                active_deprecations_target='active-deprecations')
    class deprecated_class_new:
        def __new__(cls, arg):
            return arg

    with warns_deprecated_sympy():
        assert deprecated_class_new(1) == 1

    @deprecated('deprecated_class_init is deprecated',
                deprecated_since_version='1.10',
                active_deprecations_target='active-deprecations')
    class deprecated_class_init:
        def __init__(self, arg):
            self.arg = 1

    with warns_deprecated_sympy():
        assert deprecated_class_init(1).arg == 1

    @deprecated('deprecated_class_new_init is deprecated',
                deprecated_since_version='1.10',
                active_deprecations_target='active-deprecations')
    class deprecated_class_new_init:
        def __new__(cls, arg):
            if arg == 0:
                return arg
            return object.__new__(cls)

        def __init__(self, arg):
            self.arg = 1

    with warns_deprecated_sympy():
        assert deprecated_class_new_init(0) == 0

    with warns_deprecated_sympy():
        assert deprecated_class_new_init(1).arg == 1


def test_deprecated():
    # Maintain tests for deprecated functions.  We must capture
    # the deprecation warnings.  When the deprecated functionality is
    # removed, the corresponding tests should be removed.

    m = Matrix(3, 3, [0, 1, 0, -4, 4, 0, -2, 1, 2])
    P, Jcells = m.jordan_cells()
    assert Jcells[1] == Matrix(1, 1, [2])
    assert Jcells[0] == Matrix(2, 2, [2, 1, 0, 2])


def test_deprecated():
    # Maintain tests for deprecated functions.  We must capture
    # the deprecation warnings.  When the deprecated functionality is
    # removed, the corresponding tests should be removed.

    m = Matrix(3, 3, [0, 1, 0, -4, 4, 0, -2, 1, 2])
    P, Jcells = m.jordan_cells()
    assert Jcells[1] == Matrix(1, 1, [2])
    assert Jcells[0] == Matrix(2, 2, [2, 1, 0, 2])


def test_deprecated():
    with warns_deprecated_sympy():
        cs_wname = CoordSystem('cs', p, ['a', 'b'])
        assert cs_wname == cs_wname.func(*cs_wname.args)

