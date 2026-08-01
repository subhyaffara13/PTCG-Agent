
def _remove_set(ob, attrs):
    """
    Include only attrs that are None in ob.
    """
    return {key: value for key, value in attrs.items() if getattr(ob, key) is None}

