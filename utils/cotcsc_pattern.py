
def cotcsc_pattern(symbol):
    a, b, m, n = make_wilds(symbol)
    pattern = cot(a*symbol)**m * csc(b*symbol)**n

    return pattern, a, b, m, n

