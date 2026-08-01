
def zero_mul_simp(l, index):
    """Used to combine two reduced words."""
    while index >=0 and index < len(l) - 1 and l[index][0] == l[index + 1][0]:
        exp = l[index][1] + l[index + 1][1]
        base = l[index][0]
        l[index] = (base, exp)
        del l[index + 1]
        if l[index][1] == 0:
            del l[index]
            index -= 1

