
def gmpy_bitcount(n):
    """Calculate bit size of the nonnegative integer n."""
    if n: return MPZ(n).numdigits(2)
    else: return 0

