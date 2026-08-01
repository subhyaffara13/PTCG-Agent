
def _cs_subset_subroutines(charstring, subrs, gsubrs):
    p = charstring.program
    for i in range(1, len(p)):
        if p[i] == "callsubr":
            assert isinstance(p[i - 1], int)
            p[i - 1] = subrs._used.index(p[i - 1] + subrs._old_bias) - subrs._new_bias
        elif p[i] == "callgsubr":
            assert isinstance(p[i - 1], int)
            p[i - 1] = (
                gsubrs._used.index(p[i - 1] + gsubrs._old_bias) - gsubrs._new_bias
            )

