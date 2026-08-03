from typing import Tuple

def _simplify_patterns_and3():
    """ Three-term patterns for And."""

    from sympy.core import Wild
    from sympy.core.relational import Eq, Ge, Gt

    a = Wild('a')
    b = Wild('b')
    c = Wild('c')
    # Relationals patterns should be in alphabetical order
    # (pattern1, pattern2, pattern3, simplified)
    # Do not use Le, Lt
    _matchers_and = ((Tuple(Ge(a, b), Ge(b, c), Gt(c, a)), false),
                     (Tuple(Ge(a, b), Gt(b, c), Gt(c, a)), false),
                     (Tuple(Gt(a, b), Gt(b, c), Gt(c, a)), false),
                     # (Tuple(Ge(c, a), Gt(a, b), Gt(b, c)), S.false),
                     # Lower bound relations
                     # Commented out combinations that does not simplify
                     (Tuple(Ge(a, b), Ge(a, c), Ge(b, c)), And(Ge(a, b), Ge(b, c))),
                     (Tuple(Ge(a, b), Ge(a, c), Gt(b, c)), And(Ge(a, b), Gt(b, c))),
                     # (Tuple(Ge(a, b), Gt(a, c), Ge(b, c)), And(Ge(a, b), Ge(b, c))),
                     (Tuple(Ge(a, b), Gt(a, c), Gt(b, c)), And(Ge(a, b), Gt(b, c))),
                     # (Tuple(Gt(a, b), Ge(a, c), Ge(b, c)), And(Gt(a, b), Ge(b, c))),
                     (Tuple(Ge(a, c), Gt(a, b), Gt(b, c)), And(Gt(a, b), Gt(b, c))),
                     (Tuple(Ge(b, c), Gt(a, b), Gt(a, c)), And(Gt(a, b), Ge(b, c))),
                     (Tuple(Gt(a, b), Gt(a, c), Gt(b, c)), And(Gt(a, b), Gt(b, c))),
                     # Upper bound relations
                     # Commented out combinations that does not simplify
                     (Tuple(Ge(b, a), Ge(c, a), Ge(b, c)), And(Ge(c, a), Ge(b, c))),
                     (Tuple(Ge(b, a), Ge(c, a), Gt(b, c)), And(Ge(c, a), Gt(b, c))),
                     # (Tuple(Ge(b, a), Gt(c, a), Ge(b, c)), And(Gt(c, a), Ge(b, c))),
                     (Tuple(Ge(b, a), Gt(c, a), Gt(b, c)), And(Gt(c, a), Gt(b, c))),
                     # (Tuple(Gt(b, a), Ge(c, a), Ge(b, c)), And(Ge(c, a), Ge(b, c))),
                     (Tuple(Ge(c, a), Gt(b, a), Gt(b, c)), And(Ge(c, a), Gt(b, c))),
                     (Tuple(Ge(b, c), Gt(b, a), Gt(c, a)), And(Gt(c, a), Ge(b, c))),
                     (Tuple(Gt(b, a), Gt(c, a), Gt(b, c)), And(Gt(c, a), Gt(b, c))),
                     # Circular relation
                     (Tuple(Ge(a, b), Ge(b, c), Ge(c, a)), And(Eq(a, b), Eq(b, c))),
                     )
    return _matchers_and

