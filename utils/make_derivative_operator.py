
def make_derivative_operator(M, z):
    """ Create a derivative operator, to be passed to Operator.apply. """
    def doit(C):
        r = z*C.diff(z) + C*M
        r = r.applyfunc(make_simp(z))
        return r
    return doit

