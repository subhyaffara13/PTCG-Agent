
def solve_aux_eq(numa, dena, numy, deny, x, m):
    """
    Helper function to find a polynomial solution
    of degree m for the auxiliary differential
    equation.
    """
    # Assume that the solution is of the type
    # p(x) = C_0 + C_1*x + ... + C_{m-1}*x**(m-1) + x**m
    psyms = symbols(f'C0:{m}', cls=Dummy)
    K = ZZ[psyms]
    psol = Poly(K.gens, x, domain=K) + Poly(x**m, x, domain=K)

    # Eq (5.16) in Thesis - Pg 81
    auxeq = (dena*(numy.diff(x)*deny - numy*deny.diff(x) + numy**2) - numa*deny**2)*psol
    if m >= 1:
        px = psol.diff(x)
        auxeq += px*(2*numy*deny*dena)
    if m >= 2:
        auxeq += px.diff(x)*(deny**2*dena)
    if m != 0:
        # m is a non-zero integer. Find the constant terms using undetermined coefficients
        return psol, linsolve_dict(auxeq.all_coeffs(), psyms), True
    else:
        # m == 0 . Check if 1 (x**0) is a solution to the auxiliary equation
        return S.One, auxeq, auxeq == 0

