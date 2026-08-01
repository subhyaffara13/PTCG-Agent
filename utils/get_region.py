
def get_region(z):
    """Assign numbers for regions where hyp2f1 must be handled differently."""
    if z == 1 + 0j:
        return 0
    elif abs(z) < 0.9 and z.real >= 0:
        return 1
    elif abs(z) <= 1 and z.real < 0:
        return 2
    elif 0.9 <= abs(z) <= 1 and abs(1 - z) < 0.9:
        return 3
    elif 0.9 <= abs(z) <= 1 and abs(1 - z) >= 0.9:
        return 4
    elif 1 < abs(z) < 1.1 and abs(1 - z) >= 0.9 and z.real >= 0:
        return 5
    else:
        return 6

