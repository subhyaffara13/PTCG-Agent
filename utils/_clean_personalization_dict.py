
def _clean_personalization_dict(personalization):
    """Filter out zero values from the personalization dictionary,
    handle case where None is passed, ensure values are non-negative."""
    if personalization is None:
        return {}
    if any(value < 0 for value in personalization.values()):
        raise nx.NetworkXAlgorithmError("Personalization values must be non-negative.")
    return {node: value for node, value in personalization.items() if value != 0}

