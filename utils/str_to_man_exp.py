
def str_to_man_exp(x, base=10):
    """Helper function for from_str."""
    x = x.lower().rstrip('l')
    # Verify that the input is a valid float literal
    float(x)
    # Split into mantissa, exponent
    parts = x.split('e')
    if len(parts) == 1:
        exp = 0
    else: # == 2
        x = parts[0]
        exp = int(parts[1])
    # Look for radix point in mantissa
    parts = x.split('.')
    if len(parts) == 2:
        a, b = parts[0], parts[1].rstrip('0')
        exp -= len(b)
        x = a + b
    x = MPZ(int(x, base))
    return x, exp

