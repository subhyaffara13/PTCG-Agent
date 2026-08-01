
def test_poly_hypothesis_rationals(f_q, g_q):
    remainder_q = f_q.rem(g_q)
    assert g_q.degree() >= remainder_q.degree() or remainder_q.degree() == 0

