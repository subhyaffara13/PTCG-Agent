
def _norminvgauss_quadrature(x, y, a, b):
    # gh-23196 reported that the norminvgauss CDF would drop to zero in the far right
    # tail. The SF had a similar problem, dropping to zero at the far left.
    # This fixes the bug by using 1 - SF to compute the CDF in the right tail and
    # 1 - CDF to compute the SF in the left tail. The mean is guaranteed to be beyond
    # the median, so there is no loss of precision due to subtractive cancellation.
    mean = b / np.sqrt((a + b) * (a - b))
    if np.isneginf(x) and y > abs(mean):
        return 1 - integrate.quad(norminvgauss._pdf, y, np.inf, args=(a, b))[0]
    if np.isposinf(y) and x < -abs(mean):
        return 1 - integrate.quad(norminvgauss._pdf, -np.inf, x, args=(a, b))[0]
    else:
        res = integrate.quad(norminvgauss._pdf, x, y, args=(a, b))[0]
    return np.clip(res, 0, 1)

