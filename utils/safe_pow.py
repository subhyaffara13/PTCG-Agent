
def safe_pow(base, exp):
    sign = 1
    if base < 0:
        base = -base
        sign = 1 if exp % 2 == 0 else -1
    return sign * _safe_pow(base, exp)

