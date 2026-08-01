
def _corem(eq, c):  # helper for extract_additively
    # return co, diff from co*c + diff
    co = []
    non = []
    for i in Add.make_args(eq):
        ci = i.coeff(c)
        if not ci:
            non.append(i)
        else:
            co.append(ci)
    return Add(*co), Add(*non)

