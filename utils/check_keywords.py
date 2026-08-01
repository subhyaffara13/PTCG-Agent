
def check_keywords(sig):
    num_pos_only, func, keyword_exclude, sigspec = sig
    if keyword_exclude:
        return True
    return has_keywords(func, sigspec)

