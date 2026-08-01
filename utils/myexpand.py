
def myexpand(func, target):
    expanded = expand_func(func)
    if target is not None:
        return expanded == target
    if expanded == func:  # it didn't expand
        return False

    # check to see that the expanded and original evaluate to the same value
    subs = {}
    for a in func.free_symbols:
        subs[a] = randcplx()
    return abs(func.subs(subs).n()
               - expanded.replace(exp_polar, exp).subs(subs).n()) < 1e-10

