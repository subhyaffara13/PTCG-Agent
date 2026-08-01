
def random_weighted_sample(mapping, k, seed=None):
    """Returns k items without replacement from a weighted sample.

    The input is a dictionary of items with weights as values.
    """
    if k > len(mapping):
        raise ValueError("sample larger than population")
    sample = set()
    while len(sample) < k:
        sample.add(weighted_choice(mapping, seed))
    return list(sample)

