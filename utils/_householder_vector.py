
def _householder_vector(x):
    if not x.cols == 1:
        raise ValueError("Input must be a column matrix")
    v = x.copy()
    v_plus = x.copy()
    v_minus = x.copy()
    q = x[0, 0] / abs(x[0, 0])
    norm_x = x.norm()
    v_plus[0, 0] = x[0, 0] + q * norm_x
    v_minus[0, 0] = x[0, 0] - q * norm_x
    if x[1:, 0].norm() == 0:
        bet = 0
        v[0, 0] = 1
    else:
        if v_plus.norm() <= v_minus.norm():
            v = v_plus
        else:
            v = v_minus
        v = v / v[0]
        bet = 2 / (v.norm() ** 2)
    return v, bet

