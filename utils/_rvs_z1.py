
def _rvs_Z1(alpha, beta, size=None, random_state=None):
    """Simulate random variables using Nolan's methods as detailed in [NO].
    """

    def alpha1func(alpha, beta, TH, aTH, bTH, cosTH, tanTH, W):
        return (
            2
            / np.pi
            * (
                (np.pi / 2 + bTH) * tanTH
                - beta * np.log((np.pi / 2 * W * cosTH) / (np.pi / 2 + bTH))
            )
        )

    def beta0func(alpha, beta, TH, aTH, bTH, cosTH, tanTH, W):
        return (
            W
            / (cosTH / np.tan(aTH) + np.sin(TH))
            * ((np.cos(aTH) + np.sin(aTH) * tanTH) / W) ** (1.0 / alpha)
        )

    def otherwise(alpha, beta, TH, aTH, bTH, cosTH, tanTH, W):
        # alpha is not 1 and beta is not 0
        val0 = beta * np.tan(np.pi * alpha / 2)
        th0 = np.arctan(val0) / alpha
        val3 = W / (cosTH / np.tan(alpha * (th0 + TH)) + np.sin(TH))
        res3 = val3 * (
            (
                np.cos(aTH)
                + np.sin(aTH) * tanTH
                - val0 * (np.sin(aTH) - np.cos(aTH) * tanTH)
            )
            / W
        ) ** (1.0 / alpha)
        return res3

    def alphanot1func(alpha, beta, TH, aTH, bTH, cosTH, tanTH, W):
        return xpx.apply_where(
            beta == 0, (alpha, beta, TH, aTH, bTH, cosTH, tanTH, W),
            beta0func, otherwise)

    alpha = np.broadcast_to(alpha, size)
    beta = np.broadcast_to(beta, size)
    TH = uniform.rvs(
        loc=-np.pi / 2.0, scale=np.pi, size=size, random_state=random_state
    )
    W = expon.rvs(size=size, random_state=random_state)
    aTH = alpha * TH
    bTH = beta * TH
    cosTH = np.cos(TH)
    tanTH = np.tan(TH)
    return xpx.apply_where(
        alpha == 1, (alpha, beta, TH, aTH, bTH, cosTH, tanTH, W),
        alpha1func, alphanot1func)

