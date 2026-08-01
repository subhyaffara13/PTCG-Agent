
def check_required_args(sig):
    num_pos_only, func, keyword_exclude, sigspec = sig
    return num_required_args(func, sigspec)

