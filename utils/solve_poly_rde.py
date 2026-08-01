
def solve_poly_rde(b, cQ, n, DE, parametric=False):
    """
    Solve a Polynomial Risch Differential Equation with degree bound ``n``.

    This constitutes step 4 of the outline given in the rde.py docstring.

    For parametric=False, cQ is c, a Poly; for parametric=True, cQ is Q ==
    [q1, ..., qm], a list of Polys.
    """
    # No cancellation
    if not b.is_zero and (DE.case == 'base' or
            b.degree(DE.t) > max(0, DE.d.degree(DE.t) - 1)):

        if parametric:
            # Delayed imports
            from .prde import prde_no_cancel_b_large
            return prde_no_cancel_b_large(b, cQ, n, DE)
        return no_cancel_b_large(b, cQ, n, DE)

    elif (b.is_zero or b.degree(DE.t) < DE.d.degree(DE.t) - 1) and \
            (DE.case == 'base' or DE.d.degree(DE.t) >= 2):

        if parametric:
            from .prde import prde_no_cancel_b_small
            return prde_no_cancel_b_small(b, cQ, n, DE)

        R = no_cancel_b_small(b, cQ, n, DE)

        if isinstance(R, Poly):
            return R
        else:
            # XXX: Might k be a field? (pg. 209)
            h, b0, c0 = R
            with DecrementLevel(DE):
                b0, c0 = b0.as_poly(DE.t), c0.as_poly(DE.t)
                if b0 is None:  # See above comment
                    raise ValueError("b0 should be a non-Null value")
                if c0 is  None:
                    raise ValueError("c0 should be a non-Null value")
                y = solve_poly_rde(b0, c0, n, DE).as_poly(DE.t)
            return h + y

    elif DE.d.degree(DE.t) >= 2 and b.degree(DE.t) == DE.d.degree(DE.t) - 1 and \
            n > -b.as_poly(DE.t).LC()/DE.d.as_poly(DE.t).LC():

        # TODO: Is this check necessary, and if so, what should it do if it fails?
        # b comes from the first element returned from spde()
        if not b.as_poly(DE.t).LC().is_number:
            raise TypeError("Result should be a number")

        if parametric:
            raise NotImplementedError("prde_no_cancel_b_equal() is not yet "
                "implemented.")

        R = no_cancel_equal(b, cQ, n, DE)

        if isinstance(R, Poly):
            return R
        else:
            h, m, C = R
            # XXX: Or should it be rischDE()?
            y = solve_poly_rde(b, C, m, DE)
            return h + y

    else:
        # Cancellation
        if b.is_zero:
            raise NotImplementedError("Remaining cases for Poly (P)RDE are "
            "not yet implemented (is_deriv_in_field() required).")
        else:
            if DE.case == 'exp':
                if parametric:
                    raise NotImplementedError("Parametric RDE cancellation "
                        "hyperexponential case is not yet implemented.")
                return cancel_exp(b, cQ, n, DE)

            elif DE.case == 'primitive':
                if parametric:
                    raise NotImplementedError("Parametric RDE cancellation "
                        "primitive case is not yet implemented.")
                return cancel_primitive(b, cQ, n, DE)

            else:
                raise NotImplementedError("Other Poly (P)RDE cancellation "
                    "cases are not yet implemented (%s)." % DE.case)

        if parametric:
            raise NotImplementedError("Remaining cases for Poly PRDE not yet "
                "implemented.")
        raise NotImplementedError("Remaining cases for Poly RDE not yet "
            "implemented.")

