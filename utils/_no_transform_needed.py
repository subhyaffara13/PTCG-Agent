
def _no_transform_needed(annotation: type) -> bool:
    return annotation == float or annotation == int

