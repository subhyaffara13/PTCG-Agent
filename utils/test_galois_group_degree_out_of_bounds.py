
def test_galois_group_degree_out_of_bounds():
    raises(ValueError, lambda: galois_group(Poly(0, x)))
    raises(ValueError, lambda: galois_group(Poly(1, x)))
    raises(ValueError, lambda: galois_group(Poly(x ** 7 + 1)))

