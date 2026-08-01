
def is_strong_bpsw_prp(n):
    if n < 1:
        raise ValueError("is_strong_bpsw_prp() requires 'n' be greater than 0")
    if n == 1:
        return False
    if n % 2 == 0:
        return n == 2
    return _is_strong_prp(n, 2) and _is_strong_selfridge_prp(n)

