
def test_deserialized_poly_equals_original():
    poly = Poly(x + y, x, y, z)
    deserialized = pickle.loads(pickle.dumps(poly))
    assert poly == deserialized, (
        "Deserialized polynomial not equal to original.")
    assert poly.gens == deserialized.gens, (
        "Deserialized polynomial has different generators than original.")

