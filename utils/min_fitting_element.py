
def min_fitting_element(start: int, step: int, lower_limit: int) -> int:
    """Returns the smallest element greater than or equal to the limit"""
    no_steps = -(-(lower_limit - start) // abs(step))
    return start + abs(step) * no_steps

