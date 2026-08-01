
def _simplify_patterns_xor():
    """ Two-term patterns for Xor."""

    from sympy.functions.elementary.miscellaneous import Min, Max
    from sympy.core import Wild
    from sympy.core.relational import Eq, Ne, Ge, Gt, Le, Lt
    a = Wild('a')
    b = Wild('b')
    c = Wild('c')
    # Relationals patterns should be in alphabetical order
    # (pattern1, pattern2, simplified)
    # Do not use Ge, Gt
    _matchers_xor = (#(Tuple(Le(b, a), Lt(a, b)), true),
                     #(Tuple(Lt(b, a), Le(a, b)), true),
                     #(Tuple(Eq(a, b), Le(b, a)), Gt(a, b)),
                     #(Tuple(Eq(a, b), Lt(b, a)), Ge(a, b)),
                     (Tuple(Eq(a, b), Le(a, b)), Lt(a, b)),
                     (Tuple(Eq(a, b), Lt(a, b)), Le(a, b)),
                     (Tuple(Le(a, b), Lt(a, b)), Eq(a, b)),
                     (Tuple(Le(a, b), Le(b, a)), Ne(a, b)),
                     (Tuple(Le(b, a), Ne(a, b)), Le(a, b)),
                     # (Tuple(Lt(b, a), Lt(a, b)), Ne(a, b)),
                     (Tuple(Lt(b, a), Ne(a, b)), Lt(a, b)),
                     # (Tuple(Le(a, b), Lt(a, b)), Eq(a, b)),
                     # (Tuple(Le(a, b), Ne(a, b)), Ge(a, b)),
                     # (Tuple(Lt(a, b), Ne(a, b)), Gt(a, b)),
                     # Min/Max/ITE
                     (Tuple(Le(b, a), Le(c, a)),
                      And(Ge(a, Min(b, c)), Lt(a, Max(b, c)))),
                     (Tuple(Le(b, a), Lt(c, a)),
                      ITE(b > c, And(Gt(a, c), Lt(a, b)),
                          And(Ge(a, b), Le(a, c)))),
                     (Tuple(Lt(b, a), Lt(c, a)),
                      And(Gt(a, Min(b, c)), Le(a, Max(b, c)))),
                     (Tuple(Le(a, b), Le(a, c)),
                      And(Le(a, Max(b, c)), Gt(a, Min(b, c)))),
                     (Tuple(Le(a, b), Lt(a, c)),
                      ITE(b < c, And(Lt(a, c), Gt(a, b)),
                          And(Le(a, b), Ge(a, c)))),
                     (Tuple(Lt(a, b), Lt(a, c)),
                      And(Lt(a, Max(b, c)), Ge(a, Min(b, c)))),
                     )
    return _matchers_xor

