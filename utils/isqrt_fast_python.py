
def isqrt_fast_python(x):
    """
    Fast approximate integer square root, computed using division-free
    Newton iteration for large x. For random integers the result is almost
    always correct (floor(sqrt(x))), but is 1 ulp too small with a roughly
    0.1% probability. If x is very close to an exact square, the answer is
    1 ulp wrong with high probability.

    With 0 guard bits, the largest error over a set of 10^5 random
    inputs of size 1-10^5 bits was 3 ulp. The use of 10 guard bits
    almost certainly guarantees a max 1 ulp error.
    """
    # Use direct division-based iteration if sqrt(x) < 2^400
    # Assume floating-point square root accurate to within 1 ulp, then:
    # 0 Newton iterations good to 52 bits
    # 1 Newton iterations good to 104 bits
    # 2 Newton iterations good to 208 bits
    # 3 Newton iterations good to 416 bits
    if x < _1_800:
        y = int(x**0.5)
        if x >= _1_100:
            y = (y + x//y) >> 1
            if x >= _1_200:
                y = (y + x//y) >> 1
                if x >= _1_400:
                    y = (y + x//y) >> 1
        return y
    bc = bitcount(x)
    guard_bits = 10
    x <<= 2*guard_bits
    bc += 2*guard_bits
    bc += (bc&1)
    hbc = bc//2
    startprec = min(50, hbc)
    # Newton iteration for 1/sqrt(x), with floating-point starting value
    r = int(2.0**(2*startprec) * (x >> (bc-2*startprec)) ** -0.5)
    pp = startprec
    for p in giant_steps(startprec, hbc):
        # r**2, scaled from real size 2**(-bc) to 2**p
        r2 = (r*r) >> (2*pp - p)
        # x*r**2, scaled from real size ~1.0 to 2**p
        xr2 = ((x >> (bc-p)) * r2) >> p
        # New value of r, scaled from real size 2**(-bc/2) to 2**p
        r = (r * ((3<<p) - xr2)) >> (pp+1)
        pp = p
    # (1/sqrt(x))*x = sqrt(x)
    return (r*(x>>hbc)) >> (p+guard_bits)

