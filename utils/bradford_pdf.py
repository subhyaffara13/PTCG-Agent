
def bradford_pdf(x, c):
    if 0 <= x <= 1:
        return 1.0 / (1.0 + c * x)
    return 0.0

