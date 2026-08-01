
def residue_reduce_derivation(H, DE, z):
    """
    Computes the derivation of an expression returned by residue_reduce().

    In general, this is a rational function in t, so this returns an
    as_expr() result.
    """
    # TODO: verify that this is correct for multiple extensions
    i = Dummy('i')
    return S(sum(RootSum(a[0].as_poly(z), Lambda(i, i*derivation(a[1],
        DE).as_expr().subs(z, i)/a[1].as_expr().subs(z, i))) for a in H))

