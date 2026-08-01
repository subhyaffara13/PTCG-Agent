
def betaprime_pdf(x, a, b):
    if x > 0:
        logf = (a - 1) * math.log(x) - (a + b) * math.log1p(x) - sc.betaln(a, b)
        return math.exp(logf)
    else:
        # return pdf at x == 0 separately to avoid runtime warnings
        if a > 1:
            return 0
        elif a < 1:
            return np.inf
        else:
            return 1 / sc.beta(a, b)

