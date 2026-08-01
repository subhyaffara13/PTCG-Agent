
def residue_reduce_to_basic(H, DE, z):
    """
    Converts the tuple returned by residue_reduce() into a Basic expression.
    """
    # TODO: check what Lambda does with RootOf
    i = Dummy('i')
    s = list(zip(reversed(DE.T), reversed([f(DE.x) for f in DE.Tfuncs])))

    return sum(RootSum(a[0].as_poly(z), Lambda(i, i*log(a[1].as_expr()).subs(
        {z: i}).subs(s))) for a in H)

