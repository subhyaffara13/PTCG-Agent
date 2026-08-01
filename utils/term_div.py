
def term_div(a, b, domain):
    """Division of two terms in over a ring/field. """
    a_lm, a_lc = a
    b_lm, b_lc = b

    monom = monomial_div(a_lm, b_lm)

    if domain.is_Field:
        if monom is not None:
            return monom, domain.quo(a_lc, b_lc)
        else:
            return None
    else:
        if not (monom is None or a_lc % b_lc):
            return monom, domain.quo(a_lc, b_lc)
        else:
            return None

