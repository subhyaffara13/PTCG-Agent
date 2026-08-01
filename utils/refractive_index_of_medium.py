
def refractive_index_of_medium(medium):
    """
    Helper function that returns refractive index, given a medium
    """
    if isinstance(medium, Medium):
        n = medium.refractive_index
    else:
        n = sympify(medium)
    return n

