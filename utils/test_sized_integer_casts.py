
def test_sized_integer_casts(bitsize, signed):
    idtype = f"int{bitsize}"
    if signed:
        inp = [-(2**p - 1) for p in reversed(range(bitsize - 1))]
        inp += [2**p - 1 for p in range(1, bitsize - 1)]
    else:
        idtype = "u" + idtype
        inp = [2**p - 1 for p in range(bitsize)]
    ainp = np.array(inp, dtype=idtype)
    assert_array_equal(ainp, ainp.astype("T").astype(idtype))

    # safe casting works
    ainp.astype("T", casting="safe")

    with pytest.raises(TypeError):
        ainp.astype("T").astype(idtype, casting="safe")

    oob = [str(2**bitsize), str(-(2**bitsize))]
    with pytest.raises(OverflowError):
        np.array(oob, dtype="T").astype(idtype)

    with pytest.raises(ValueError):
        np.array(["1", np.nan, "3"],
                 dtype=StringDType(na_object=np.nan)).astype(idtype)

