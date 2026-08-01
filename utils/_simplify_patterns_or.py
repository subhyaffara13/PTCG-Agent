
def _simplify_patterns_or():
    """ Two-term patterns for Or."""

    from sympy.core import Wild
    from sympy.core.relational import Eq, Ne, Ge, Gt, Le, Lt
    from sympy.functions.elementary.complexes import Abs
    from sympy.functions.elementary.miscellaneous import Min, Max
    a = Wild('a')
    b = Wild('b')
    c = Wild('c')
    # Relationals patterns should be in alphabetical order
    # (pattern1, pattern2, simplified)
    # Do not use Ge, Gt
    _matchers_or = ((Tuple(Le(b, a), Le(a, b)), true),
                    #(Tuple(Le(b, a), Lt(a, b)), true),
                    (Tuple(Le(b, a), Ne(a, b)), true),
                    #(Tuple(Le(a, b), Lt(b, a)), true),
                    #(Tuple(Le(a, b), Ne(a, b)), true),
                    #(Tuple(Eq(a, b), Le(b, a)), Ge(a, b)),
                    #(Tuple(Eq(a, b), Lt(b, a)), Ge(a, b)),
                    (Tuple(Eq(a, b), Le(a, b)), Le(a, b)),
                    (Tuple(Eq(a, b), Lt(a, b)), Le(a, b)),
                    #(Tuple(Le(b, a), Lt(b, a)), Ge(a, b)),
                    (Tuple(Lt(b, a), Lt(a, b)), Ne(a, b)),
                    (Tuple(Lt(b, a), Ne(a, b)), Ne(a, b)),
                    (Tuple(Le(a, b), Lt(a, b)), Le(a, b)),
                    #(Tuple(Lt(a, b), Ne(a, b)), Ne(a, b)),
                    (Tuple(Eq(a, b), Ne(a, c)), ITE(Eq(b, c), true, Ne(a, c))),
                    (Tuple(Ne(a, b), Ne(a, c)), ITE(Eq(b, c), Ne(a, b), true)),
                    # Min/Max/ITE
                    (Tuple(Le(b, a), Le(c, a)), Ge(a, Min(b, c))),
                    #(Tuple(Ge(b, a), Ge(c, a)), Ge(Min(b, c), a)),
                    (Tuple(Le(b, a), Lt(c, a)), ITE(b > c, Lt(c, a), Le(b, a))),
                    (Tuple(Lt(b, a), Lt(c, a)), Gt(a, Min(b, c))),
                    #(Tuple(Gt(b, a), Gt(c, a)), Gt(Min(b, c), a)),
                    (Tuple(Le(a, b), Le(a, c)), Le(a, Max(b, c))),
                    #(Tuple(Le(b, a), Le(c, a)), Le(Max(b, c), a)),
                    (Tuple(Le(a, b), Lt(a, c)), ITE(b >= c, Le(a, b), Lt(a, c))),
                    (Tuple(Lt(a, b), Lt(a, c)), Lt(a, Max(b, c))),
                    #(Tuple(Lt(b, a), Lt(c, a)), Lt(Max(b, c), a)),
                    (Tuple(Le(a, b), Le(c, a)), ITE(b >= c, true, Or(Le(a, b), Ge(a, c)))),
                    (Tuple(Le(c, a), Le(a, b)), ITE(b >= c, true, Or(Le(a, b), Ge(a, c)))),
                    (Tuple(Lt(a, b), Lt(c, a)), ITE(b > c, true, Or(Lt(a, b), Gt(a, c)))),
                    (Tuple(Lt(c, a), Lt(a, b)), ITE(b > c, true, Or(Lt(a, b), Gt(a, c)))),
                    (Tuple(Le(a, b), Lt(c, a)), ITE(b >= c, true, Or(Le(a, b), Gt(a, c)))),
                    (Tuple(Le(c, a), Lt(a, b)), ITE(b >= c, true, Or(Lt(a, b), Ge(a, c)))),
                    (Tuple(Lt(b, a), Lt(a, -b)), ITE(b >= 0, Gt(Abs(a), b), true)),
                    (Tuple(Le(b, a), Le(a, -b)), ITE(b > 0, Ge(Abs(a), b), true)),
                    )
    return _matchers_or

