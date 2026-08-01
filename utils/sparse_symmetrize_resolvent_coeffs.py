
def sparse_symmetrize_resolvent_coeffs(F, X, s, verbose=False):
    """
    Compute the coefficients of a resolvent as functions of the coefficients of
    the associated polynomial.

    F must be a sparse polynomial.
    """
    import time, sys
    # Roots of resolvent as multivariate forms over vars X:
    root_forms = [
        F.compose(list(zip(X, sigma(X))))
        for sigma in s
    ]

    # Coeffs of resolvent (besides lead coeff of 1) as symmetric forms over vars X:
    Y = [Dummy(f'Y{i}') for i in range(len(s))]
    coeff_forms = []
    for i in range(1, len(s) + 1):
        if verbose:
            print('----')
            print(f'Computing symmetric poly of degree {i}...')
            sys.stdout.flush()
        t0 = time.time()
        G = symmetric_poly(i, *Y)
        t1 = time.time()
        if verbose:
            print(f'took {t1 - t0} seconds')
            print('lambdifying...')
            sys.stdout.flush()
        t0 = time.time()
        C = lambdify(Y, (-1)**i*G)
        t1 = time.time()
        if verbose:
            print(f'took {t1 - t0} seconds')
            sys.stdout.flush()
        coeff_forms.append(C)

    coeffs = []
    for i, f in enumerate(coeff_forms):
        if verbose:
            print('----')
            print(f'Plugging root forms into elem symm poly {i+1}...')
            sys.stdout.flush()
        t0 = time.time()
        g = f(*root_forms)
        t1 = time.time()
        coeffs.append(g)
        if verbose:
            print(f'took {t1 - t0} seconds')
            sys.stdout.flush()

    # Now symmetrize these coeffs. This means recasting them as polynomials in
    # the elementary symmetric polys over X.
    symmetrized = []
    symmetrization_times = []
    ss = s_vars(len(X))
    for i, A in list(enumerate(coeffs)):
        if verbose:
            print('-----')
            print(f'Coeff {i+1}...')
            sys.stdout.flush()
        t0 = time.time()
        B, rem, _ = A.symmetrize()
        t1 = time.time()
        if rem != 0:
            msg = f"Got nonzero remainder {rem} for resolvent (F, X, s) = ({F}, {X}, {s})"
            raise ResolventException(msg)
        B_str = str(B.as_expr(*ss))
        symmetrized.append(B_str)
        symmetrization_times.append(t1 - t0)
        if verbose:
            print(wrap(B_str))
            print(f'took {t1 - t0} seconds')
            sys.stdout.flush()

    return symmetrized, symmetrization_times

