
def _match_div_rewrite(expr, i):
    """helper for __trigsimp"""
    if i == 0:
        expr = _replace_mul_fpowxgpow(expr, sin, cos,
            _midn, tan, _idn)
    elif i == 1:
        expr = _replace_mul_fpowxgpow(expr, tan, cos,
            _idn, sin, _idn)
    elif i == 2:
        expr = _replace_mul_fpowxgpow(expr, cot, sin,
            _idn, cos, _idn)
    elif i == 3:
        expr = _replace_mul_fpowxgpow(expr, tan, sin,
            _midn, cos, _midn)
    elif i == 4:
        expr = _replace_mul_fpowxgpow(expr, cot, cos,
            _midn, sin, _midn)
    elif i == 5:
        expr = _replace_mul_fpowxgpow(expr, cot, tan,
            _idn, _one, _idn)
    # i in (6, 7) is skipped
    elif i == 8:
        expr = _replace_mul_fpowxgpow(expr, sinh, cosh,
            _midn, tanh, _idn)
    elif i == 9:
        expr = _replace_mul_fpowxgpow(expr, tanh, cosh,
            _idn, sinh, _idn)
    elif i == 10:
        expr = _replace_mul_fpowxgpow(expr, coth, sinh,
            _idn, cosh, _idn)
    elif i == 11:
        expr = _replace_mul_fpowxgpow(expr, tanh, sinh,
            _midn, cosh, _midn)
    elif i == 12:
        expr = _replace_mul_fpowxgpow(expr, coth, cosh,
            _midn, sinh, _midn)
    elif i == 13:
        expr = _replace_mul_fpowxgpow(expr, coth, tanh,
            _idn, _one, _idn)
    else:
        return None
    return expr

