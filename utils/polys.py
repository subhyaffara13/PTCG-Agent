
def polys(*, nonzero=False, domain="ZZ"):
    # This is a simple strategy, but sufficient the tests below
    elems = {"ZZ": st.integers(), "QQ": st.fractions()}
    coeff_st = st.lists(elems[domain])
    if nonzero:
        coeff_st = coeff_st.filter(any)
    return st.builds(Poly, coeff_st, st.just(x), domain=st.just(domain))

