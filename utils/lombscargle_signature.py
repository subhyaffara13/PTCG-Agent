
def lombscargle_signature(
    x, y, freqs, precenter=False, normalize=False, *,
    weights=None, floating_mean=False
):
    return array_namespace(x, y, freqs, weights)

