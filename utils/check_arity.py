
def check_arity(n, sig):
    num_pos_only, func, keyword_exclude, sigspec = sig
    if keyword_exclude or num_pos_only > n:
        return False
    return is_arity(n, func, sigspec)

