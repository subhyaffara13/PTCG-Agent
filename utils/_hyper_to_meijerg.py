
def _hyper_to_meijerg(func):
    """
    Converts a `hyper` to meijerg.
    """
    ap = func.ap
    bq = func.bq

    if any(i <= 0 and int(i) == i for i in ap):
        return hyperexpand(func)

    z = func.args[2]

    # parameters of the `meijerg` function.
    an = (1 - i for i in ap)
    anp = ()
    bm = (S.Zero, )
    bmq = (1 - i for i in bq)

    k = S.One

    for i in bq:
        k = k * gamma(i)

    for i in ap:
        k = k / gamma(i)

    return k * meijerg(an, anp, bm, bmq, -z)

