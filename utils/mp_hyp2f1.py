
def mp_hyp2f1(a, b, c, z):
    """Return mpmath hyp2f1 calculated on same branch as scipy hyp2f1.

    For most values of a,b,c mpmath returns the x - 0j branch of hyp2f1 on the
    branch cut x=(1,inf) whereas scipy's hyp2f1 calculates the x + 0j branch.
    Thus, to generate the right comparison values on the branch cut, we
    evaluate mpmath.hyp2f1 at x + 1e-15*j.

    The exception to this occurs when c-a=-m in which case both mpmath and
    scipy calculate the x + 0j branch on the branch cut. When this happens
    mpmath.hyp2f1 will be evaluated at the original z point.
    """
    on_branch_cut = z.real > 1.0 and abs(z.imag) < 1.0e-15
    cond1 = abs(c - a - round(c - a)) < 1.0e-15 and round(c - a) <= 0
    cond2 = abs(c - b - round(c - b)) < 1.0e-15 and round(c - b) <= 0
    # Make sure imaginary part is *exactly* zero
    if on_branch_cut:
        z = z.real + 0.0j
    if on_branch_cut and not (cond1 or cond2):
        z_mpmath = z.real + 1.0e-15j
    else:
        z_mpmath = z
    return complex(mpmath.hyp2f1(a, b, c, z_mpmath))

