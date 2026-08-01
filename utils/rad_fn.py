
def rad_fn(x, pos=None):
    """Radian function formatter."""
    n = int((x / np.pi) * 2.0 + 0.25)
    if n == 0:
        return str(x)
    elif n == 1:
        return r'$\pi/2$'
    elif n == 2:
        return r'$\pi$'
    elif n % 2 == 0:
        return fr'${n//2}\pi$'
    else:
        return fr'${n}\pi/2$'

