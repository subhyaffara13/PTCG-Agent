import copy

def test_poly_copy_equals_original():
    poly = Poly(x + y, x, y, z)
    copy = poly.copy()
    assert poly == copy, (
        "Copied polynomial not equal to original.")
    assert poly.gens == copy.gens, (
        "Copied polynomial has different generators than original.")

