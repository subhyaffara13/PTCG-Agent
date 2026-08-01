
def test_dyadic_srepr():
    from sympy.printing.repr import srepr
    N = CoordSys3D('N')

    dy = N.i | N.j
    res = "BaseDyadic(CoordSys3D(Str('N'), Tuple(ImmutableDenseMatrix([["\
        "Integer(1), Integer(0), Integer(0)], [Integer(0), Integer(1), "\
        "Integer(0)], [Integer(0), Integer(0), Integer(1)]]), "\
        "VectorZero())).i, CoordSys3D(Str('N'), Tuple(ImmutableDenseMatrix("\
        "[[Integer(1), Integer(0), Integer(0)], [Integer(0), Integer(1), "\
        "Integer(0)], [Integer(0), Integer(0), Integer(1)]]), VectorZero())).j)"
    assert srepr(dy) == res

