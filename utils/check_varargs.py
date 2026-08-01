
def check_varargs(sig):
    num_pos_only, func, keyword_exclude, sigspec = sig
    return has_varargs(func, sigspec)

