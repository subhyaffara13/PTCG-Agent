
def test_cooperative_operations():
    '''Tests that Expr uses binary operations cooperatively.

    In particular it should be possible for non-Expr classes to override
    binary operators like +, - etc when used with Expr instances. This should
    work for non-Expr classes whether they are Basic subclasses or not. Also
    non-Expr classes that do not define binary operators with Expr should give
    TypeError.
    '''
    # A bunch of instances of Expr subclasses
    exprs = [
        Expr(),
        S.Zero,
        S.One,
        S.Infinity,
        S.NegativeInfinity,
        S.ComplexInfinity,
        S.Half,
        Float(0.5),
        Integer(2),
        Symbol('x'),
        Mul(2, Symbol('x')),
        Add(2, Symbol('x')),
        Pow(2, Symbol('x')),
    ]

    for e in exprs:
        # Test that these classes can override arithmetic operations in
        # combination with various Expr types.
        for ne in [NonBasic(), NonExpr()]:

            results = [
                (ne + e, ('+', ne, e)),
                (e + ne, ('+', e, ne)),
                (ne - e, ('-', ne, e)),
                (e - ne, ('-', e, ne)),
                (ne * e, ('*', ne, e)),
                (e * ne, ('*', e, ne)),
                (ne / e, ('/', ne, e)),
                (e / ne, ('/', e, ne)),
                (ne // e, ('//', ne, e)),
                (e // ne, ('//', e, ne)),
                (ne % e, ('%', ne, e)),
                (e % ne, ('%', e, ne)),
                (divmod(ne, e), ('divmod', ne, e)),
                (divmod(e, ne), ('divmod', e, ne)),
                (ne ** e, ('**', ne, e)),
                (e ** ne, ('**', e, ne)),
                (e < ne, ('>', ne, e)),
                (ne < e, ('<', ne, e)),
                (e > ne, ('<', ne, e)),
                (ne > e, ('>', ne, e)),
                (e <= ne, ('>=', ne, e)),
                (ne <= e, ('<=', ne, e)),
                (e >= ne, ('<=', ne, e)),
                (ne >= e, ('>=', ne, e)),
            ]

            for res, args in results:
                assert type(res) is SpecialOp and res.args == args

        # These classes do not support binary operators with Expr. Every
        # operation should raise in combination with any of the Expr types.
        for na in [NonArithmetic(), object()]:

            raises(TypeError, lambda : e + na)
            raises(TypeError, lambda : na + e)
            raises(TypeError, lambda : e - na)
            raises(TypeError, lambda : na - e)
            raises(TypeError, lambda : e * na)
            raises(TypeError, lambda : na * e)
            raises(TypeError, lambda : e / na)
            raises(TypeError, lambda : na / e)
            raises(TypeError, lambda : e // na)
            raises(TypeError, lambda : na // e)
            raises(TypeError, lambda : e % na)
            raises(TypeError, lambda : na % e)
            raises(TypeError, lambda : divmod(e, na))
            raises(TypeError, lambda : divmod(na, e))
            raises(TypeError, lambda : e ** na)
            raises(TypeError, lambda : na ** e)
            raises(TypeError, lambda : e > na)
            raises(TypeError, lambda : na > e)
            raises(TypeError, lambda : e < na)
            raises(TypeError, lambda : na < e)
            raises(TypeError, lambda : e >= na)
            raises(TypeError, lambda : na >= e)
            raises(TypeError, lambda : e <= na)
            raises(TypeError, lambda : na <= e)

