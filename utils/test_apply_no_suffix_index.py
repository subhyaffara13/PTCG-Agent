
def test_apply_no_suffix_index(engine, request):
    # GH36189
    if engine == "numba":
        mark = pytest.mark.xfail(
            reason="numba engine doesn't support list-likes/dict-like callables"
        )
        request.node.add_marker(mark)
    pdf = DataFrame([[4, 9]] * 3, columns=["A", "B"])
    result = pdf.apply(["sum", lambda x: x.sum(), lambda x: x.sum()], engine=engine)
    expected = DataFrame(
        {"A": [12, 12, 12], "B": [27, 27, 27]}, index=["sum", "<lambda>", "<lambda>"]
    )

    tm.assert_frame_equal(result, expected)

