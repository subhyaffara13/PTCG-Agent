
def _fractional_power_pade_constant(i, t):
    # A helper function for matrix fractional power.
    if i < 1:
        raise ValueError('expected a positive integer i')
    if not (-1 < t < 1):
        raise ValueError('expected -1 < t < 1')
    if i == 1:
        return -t
    elif i % 2 == 0:
        j = i // 2
        return (-j + t) / (2 * (2*j - 1))
    elif i % 2 == 1:
        j = (i - 1) // 2
        return (-j - t) / (2 * (2*j + 1))
    else:
        raise Exception(f'unnexpected value of i, i = {i}')

