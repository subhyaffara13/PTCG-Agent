
def geninvgauss_mode(p, b):
    if p > 1:  # equivalent mode formulas numerical more stable versions
        return (math.sqrt((1 - p) ** 2 + b**2) - (1 - p)) / b
    return b / (math.sqrt((1 - p) ** 2 + b**2) + (1 - p))

