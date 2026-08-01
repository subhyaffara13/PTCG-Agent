
def _sqrt_numeric_denest(a, b, r, d2):
    r"""Helper that denest
    $\sqrt{a + b \sqrt{r}}, d^2 = a^2 - b^2 r > 0$

    If it cannot be denested, it returns ``None``.
    """
    d = sqrt(d2)
    s = a + d
    # sqrt_depth(res) <= sqrt_depth(s) + 1
    # sqrt_depth(expr) = sqrt_depth(r) + 2
    # there is denesting if sqrt_depth(s) + 1 < sqrt_depth(r) + 2
    # if s**2 is Number there is a fourth root
    if sqrt_depth(s) < sqrt_depth(r) + 1 or (s**2).is_Rational:
        s1, s2 = sign(s), sign(b)
        if s1 == s2 == -1:
            s1 = s2 = 1
        res = (s1 * sqrt(a + d) + s2 * sqrt(a - d)) * sqrt(2) / 2
        return res.expand()

