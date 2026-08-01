
def burr_pdf(x, cc, dd):
    # note: we use np.exp instead of math.exp, otherwise an overflow
    # error can occur in the setup, e.g., for parameters
    # 1.89128135, 0.30195177, see test test_burr_overflow
    if x > 0:
        lx = math.log(x)
        return np.exp(-(cc + 1) * lx - (dd + 1) * math.log1p(np.exp(-cc * lx)))
    else:
        return 0

