
def _laplace_trig_split(fn):
    """
    Helper function for `_laplace_rule_trig`.  This function returns two terms
    `f` and `g`.  `f` contains all product terms with sin, cos, sinh, cosh in
    them; `g` contains everything else.
    """
    trigs = [S.One]
    other = [S.One]
    for term in Mul.make_args(fn):
        if term.has(sin, cos, sinh, cosh, exp):
            trigs.append(term)
        else:
            other.append(term)
    f = Mul(*trigs)
    g = Mul(*other)
    return f, g

