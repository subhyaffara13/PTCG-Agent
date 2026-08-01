
def chi_pdf(x, a):
    if x > 0:
        return math.exp(
            (a - 1) * math.log(x)
            - 0.5 * (x * x)
            - (a / 2 - 1) * math.log(2)
            - math.lgamma(0.5 * a)
        )
    else:
        return 0 if a >= 1 else np.inf

