import math


def _range_prod(lo, hi, k=1):
    """
    Product of a range of numbers spaced k apart (from hi).

    For k=1, this returns the product of
    lo * (lo+1) * (lo+2) * ... * (hi-2) * (hi-1) * hi
    = hi! / (lo-1)!

    For k>1, it correspond to taking only every k'th number when
    counting down from hi - e.g. 18!!!! = _range_prod(1, 18, 4).

    Breaks into smaller products first for speed:
    _range_prod(2, 9) = ((2*3)*(4*5))*((6*7)*(8*9))
    """
    if lo == 1 and k == 1:
        return math.factorial(hi)

    if lo + k < hi:
        mid = (hi + lo) // 2
        if k > 1:
            # make sure mid is a multiple of k away from hi
            mid = mid - ((mid - hi) % k)
        return _range_prod(lo, mid, k) * _range_prod(mid + k, hi, k)
    elif lo + k == hi:
        return lo * hi
    else:
        return hi

