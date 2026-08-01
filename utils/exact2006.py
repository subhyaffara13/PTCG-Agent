
def exact2006(exact):
    mu0 = 4e-7 * math.pi
    c = exact['speed of light in vacuum']
    epsilon0 = 1 / (mu0 * c**2)
    replace = {
        'mag. constant': mu0,
        'electric constant': epsilon0,
        'atomic unit of permittivity': 4*math.pi*epsilon0,
        'characteristic impedance of vacuum': math.sqrt(mu0 / epsilon0),
        'hertz-inverse meter relationship': 1/c,
        'joule-kilogram relationship': 1/c**2,
        'kilogram-joule relationship': c**2,
    }
    return replace

