
def cos_17() -> Expr:
    r"""Computes $\cos \frac{\pi}{17}$ in square roots"""
    return sqrt(
        (15 + sqrt(17)) / 32 + sqrt(2) * (sqrt(17 - sqrt(17)) +
        sqrt(sqrt(2) * (-8 * sqrt(17 + sqrt(17)) - (1 - sqrt(17))
        * sqrt(17 - sqrt(17))) + 6 * sqrt(17) + 34)) / 32)

