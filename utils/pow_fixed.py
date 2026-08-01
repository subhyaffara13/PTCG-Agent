
def pow_fixed(x, n, wp):
    if n == 1:
        return x
    y = MPZ_ONE << wp
    while n:
        if n & 1:
            y = (y*x) >> wp
            n -= 1
        x = (x*x) >> wp
        n //= 2
    return y

