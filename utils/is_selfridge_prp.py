
def is_selfridge_prp(n):
    if n < 1:
        raise ValueError("is_selfridge_prp() requires 'n' be greater than 0")
    if n == 1:
        return False
    if n % 2 == 0:
        return n == 2
    return _is_selfridge_prp(n)

