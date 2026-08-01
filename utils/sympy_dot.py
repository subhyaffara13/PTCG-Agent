
def sympy_dot(seq1: Sequence[sympy.Expr], seq2: Sequence[sympy.Expr]) -> sympy.Expr:
    assert len(seq1) == len(seq2)
    return sympy.expand(sum(a * b for a, b in zip(seq1, seq2)))

