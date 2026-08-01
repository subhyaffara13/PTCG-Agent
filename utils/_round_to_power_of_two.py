
def _round_to_power_of_two(x):
    """
    Round elements of the array to the nearest power of two.
    """
    return 2**np.around(np.log2(x))

