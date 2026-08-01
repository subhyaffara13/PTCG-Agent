
def test_srepr():
    from sympy.printing.repr import srepr
    res = "CoordSys3D(Str('C'), Tuple(ImmutableDenseMatrix([[Integer(1), "\
            "Integer(0), Integer(0)], [Integer(0), Integer(1), Integer(0)], "\
            "[Integer(0), Integer(0), Integer(1)]]), VectorZero())).i"
    assert srepr(C.i) == res

