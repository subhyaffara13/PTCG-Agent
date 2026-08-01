
def _handle_poly(polys, symbols):
    # _handle_poly(polys, symbols) -> (poly_sol, poly_eqs)
    #
    # We will return possible solution information to nonlinsolve as well as a
    # new system of polynomial equations to be solved if we cannot solve
    # everything directly here. The new system of polynomial equations will be
    # a lex-order Groebner basis for the original system. The lex basis
    # hopefully separate some of the variables and equations and give something
    # easier for substitution to work with.

    # The format for representing solution sets in nonlinsolve and substitution
    # is a list of dicts. These are the special cases:
    no_information = [{}]   # No equations solved yet
    no_solutions = []       # The system is inconsistent and has no solutions.

    # If there is no need to attempt further solution of these equations then
    # we return no equations:
    no_equations = []

    inexact = any(not p.domain.is_Exact for p in polys)
    if inexact:
        # The use of Groebner over RR is likely to result incorrectly in an
        # inconsistent Groebner basis. So, convert any float coefficients to
        # Rational before computing the Groebner basis.
        polys = [poly(nsimplify(p, rational=True)) for p in polys]

    # Compute a Groebner basis in grevlex order wrt the ordering given. We will
    # try to convert this to lex order later. Usually it seems to be more
    # efficient to compute a lex order basis by computing a grevlex basis and
    # converting to lex with fglm.
    basis = groebner(polys, symbols, order='grevlex', polys=False)

    #
    # No solutions (inconsistent equations)?
    #
    if 1 in basis:

        # No solutions:
        poly_sol = no_solutions
        poly_eqs = no_equations

    #
    # Finite number of solutions (zero-dimensional case)
    #
    elif basis.is_zero_dimensional:

        # Convert Groebner basis to lex ordering
        basis = basis.fglm('lex')

        # Convert polynomial coefficients back to float before calling
        # solve_poly_system
        if inexact:
            basis = [nfloat(p) for p in basis]

        # Solve the zero-dimensional case using solve_poly_system if possible.
        # If some polynomials have factors that cannot be solved in radicals
        # then this will fail. Using solve_poly_system(..., strict=True)
        # ensures that we either get a complete solution set in radicals or
        # UnsolvableFactorError will be raised.
        try:
            result = solve_poly_system(basis, *symbols, strict=True)
        except UnsolvableFactorError:
            # Failure... not fully solvable in radicals. Return the lex-order
            # basis for substitution to handle.
            poly_sol = no_information
            poly_eqs = list(basis)
        else:
            # Success! We have a finite solution set and solve_poly_system has
            # succeeded in finding all solutions. Return the solutions and also
            # an empty list of remaining equations to be solved.
            poly_sol = [dict(zip(symbols, res)) for res in result]
            poly_eqs = no_equations

    #
    # Infinite families of solutions (positive-dimensional case)
    #
    else:
        # In this case the grevlex basis cannot be converted to lex using the
        # fglm method and also solve_poly_system cannot solve the equations. We
        # would like to return a lex basis but since we can't use fglm we
        # compute the lex basis directly here. The time required to recompute
        # the basis is generally significantly less than the time required by
        # substitution to solve the new system.
        poly_sol = no_information
        poly_eqs = list(groebner(polys, symbols, order='lex', polys=False))

        if inexact:
            poly_eqs = [nfloat(p) for p in poly_eqs]

    return poly_sol, poly_eqs

