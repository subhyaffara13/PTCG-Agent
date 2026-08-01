
def test_map_identity_mapping(index, request, using_infer_string):
    # GH#12766
    if (
        not using_infer_string
        and isinstance(index.dtype, StringDtype)
        and index.dtype.storage == "python"
    ):
        mark = pytest.mark.xfail(reason="Does not preserve dtype")
        request.applymarker(mark)

    result = index.map(lambda x: x)
    if index.dtype == object and (result.dtype in (bool, "string")):
        assert (index == result).all()
        # TODO: could work that into the 'exact="equiv"'?
        return  # FIXME: doesn't belong in this file anymore!
    tm.assert_index_equal(result, index, exact="equiv")

