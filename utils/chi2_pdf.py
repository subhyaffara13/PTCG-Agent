
def chi2_pdf(x, df):
    if x > 0:
        return math.exp(
            (df / 2 - 1) * math.log(x)
            - 0.5 * x
            - (df / 2) * math.log(2)
            - math.lgamma(0.5 * df)
        )
    else:
        return 0 if df >= 1 else np.inf

