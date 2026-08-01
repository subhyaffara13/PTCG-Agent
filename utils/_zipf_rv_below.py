
def _zipf_rv_below(gamma, xmin, threshold, seed):
    """Returns a random value chosen from the bounded Zipf distribution.

    Repeatedly draws values from the Zipf distribution until the
    threshold is met, then returns that value.
    """
    result = nx.utils.zipf_rv(gamma, xmin, seed)
    while result > threshold:
        result = nx.utils.zipf_rv(gamma, xmin, seed)
    return result

