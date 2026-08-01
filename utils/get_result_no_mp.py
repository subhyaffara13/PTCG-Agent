
def get_result_no_mp(a, b, c, z, group):
    """Get results for given parameter and value combination."""
    expected, observed = complex('nan'), hyp2f1(a, b, c, z)
    relative_error, absolute_error = float('nan'), float('nan')
    return (
        a,
        b,
        c,
        z,
        abs(z),
        get_region(z),
        group,
        expected,
        observed,
        relative_error,
        absolute_error,
    )

