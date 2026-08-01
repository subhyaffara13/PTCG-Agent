
def construct_c_case_1(num, den, x, pole):
    # Find the coefficient of 1/(x - pole)**2 in the
    # Laurent series expansion of a(x) about pole.
    num1, den1 = (num*Poly((x - pole)**2, x, extension=True)).cancel(den, include=True)
    r = (num1.subs(x, pole))/(den1.subs(x, pole))

    # If multiplicity is 2, the coefficient to be added
    # in the c-vector is c = (1 +- sqrt(1 + 4*r))/2
    if r != -S(1)/4:
        return [[(1 + sqrt(1 + 4*r))/2], [(1 - sqrt(1 + 4*r))/2]]
    return [[S.Half]]

