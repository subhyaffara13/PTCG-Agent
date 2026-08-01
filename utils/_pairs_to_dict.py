
def _pairs_to_dict(pairs):
    """Convert a list of [key, value] pairs to a dict without forcing str."""
    return {pairs[i][0]: pairs[i][1] for i in range(len(pairs))}

