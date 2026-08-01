
def test_poly_hypothesis_integers(f_z, g_z):
    remainder_z = f_z.rem(g_z)
    assert g_z.degree() >= remainder_z.degree() or remainder_z.degree() == 0

