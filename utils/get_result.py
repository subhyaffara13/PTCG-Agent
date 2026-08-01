
def get_result(a, b, c, z, group):
    """Get results for given parameter and value combination."""
    expected, observed = mp_hyp2f1(a, b, c, z), hyp2f1(a, b, c, z)
    if (
            np.isnan(observed) and np.isnan(expected) or
            expected == observed
    ):
        relative_error = 0.0
        absolute_error = 0.0
    elif np.isnan(observed):
        # Set error to infinity if result is nan when not expected to be.
        # Makes results easier to interpret.
        relative_error = float("inf")
        absolute_error = float("inf")
    else:
        absolute_error = abs(expected - observed)
        relative_error = absolute_error / abs(expected)

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

