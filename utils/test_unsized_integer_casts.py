
def test_unsized_integer_casts(typename, signed):
    idtype = f"{signed}{typename}"

    inp = [1, 2, 3, 4]
    ainp = np.array(inp, dtype=idtype)
    assert_array_equal(ainp, ainp.astype("T").astype(idtype))

