
def _simplify_patterns_and():
    """ Two-term patterns for And."""

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
    _matchers_and = ((Tuple(Eq(a, b), Lt(a, b)), false),
                     #(Tuple(Eq(a, b), Lt(b, a)), S.false),
                     #(Tuple(Le(b, a), Lt(a, b)), S.false),
                     #(Tuple(Lt(b, a), Le(a, b)), S.false),
                     (Tuple(Lt(b, a), Lt(a, b)), false),
                     (Tuple(Eq(a, b), Le(b, a)), Eq(a, b)),
                     #(Tuple(Eq(a, b), Le(a, b)), Eq(a, b)),
                     #(Tuple(Le(b, a), Lt(b, a)), Gt(a, b)),
                     (Tuple(Le(b, a), Le(a, b)), Eq(a, b)),
                     #(Tuple(Le(b, a), Ne(a, b)), Gt(a, b)),
                     #(Tuple(Lt(b, a), Ne(a, b)), Gt(a, b)),
                     (Tuple(Le(a, b), Lt(a, b)), Lt(a, b)),
                     (Tuple(Le(a, b), Ne(a, b)), Lt(a, b)),
                     (Tuple(Lt(a, b), Ne(a, b)), Lt(a, b)),
                     # Sign
                     (Tuple(Eq(a, b), Eq(a, -b)), And(Eq(a, S.Zero), Eq(b, S.Zero))),
                     # Min/Max/ITE
                     (Tuple(Le(b, a), Le(c, a)), Ge(a, Max(b, c))),
                     (Tuple(Le(b, a), Lt(c, a)), ITE(b > c, Ge(a, b), Gt(a, c))),
                     (Tuple(Lt(b, a), Lt(c, a)), Gt(a, Max(b, c))),
                     (Tuple(Le(a, b), Le(a, c)), Le(a, Min(b, c))),
                     (Tuple(Le(a, b), Lt(a, c)), ITE(b < c, Le(a, b), Lt(a, c))),
                     (Tuple(Lt(a, b), Lt(a, c)), Lt(a, Min(b, c))),
                     (Tuple(Le(a, b), Le(c, a)), ITE(Eq(b, c), Eq(a, b), ITE(b < c, false, And(Le(a, b), Ge(a, c))))),
                     (Tuple(Le(c, a), Le(a, b)), ITE(Eq(b, c), Eq(a, b), ITE(b < c, false, And(Le(a, b), Ge(a, c))))),
                     (Tuple(Lt(a, b), Lt(c, a)), ITE(b < c, false, And(Lt(a, b), Gt(a, c)))),
                     (Tuple(Lt(c, a), Lt(a, b)), ITE(b < c, false, And(Lt(a, b), Gt(a, c)))),
                     (Tuple(Le(a, b), Lt(c, a)), ITE(b <= c, false, And(Le(a, b), Gt(a, c)))),
                     (Tuple(Le(c, a), Lt(a, b)), ITE(b <= c, false, And(Lt(a, b), Ge(a, c)))),
                     (Tuple(Eq(a, b), Eq(a, c)), ITE(Eq(b, c), Eq(a, b), false)),
                     (Tuple(Lt(a, b), Lt(-b, a)), ITE(b > 0, Lt(Abs(a), b), false)),
                     (Tuple(Le(a, b), Le(-b, a)), ITE(b >= 0, Le(Abs(a), b), false)),
                     )
    return _matchers_and

