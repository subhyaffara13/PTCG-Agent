
def to_linear(c):
    a = 0.055

    if c > 0.04045:
        return (math.pow((c + a) / (1.0 + a), 2.4))
    else:
        return (c / 12.92)

