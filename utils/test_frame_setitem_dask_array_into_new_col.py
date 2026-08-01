
def test_frame_setitem_dask_array_into_new_col(request):
    # GH#47128

    # dask sets "compute.use_numexpr" to False, so catch the current value
    # and ensure to reset it afterwards to avoid impacting other tests
    olduse = pd.get_option("compute.use_numexpr")

    try:
        dask = pytest.importorskip("dask")
        da = pytest.importorskip("dask.array")
        if Version(dask.__version__) <= Version("2025.1.0") and Version(
            np.__version__
        ) >= Version("2.1"):
            request.applymarker(
                pytest.mark.xfail(reason="loc.__setitem__ incorrectly mutated column c")
            )

        dda = da.array([1, 2])
        df = DataFrame({"a": ["a", "b"]})
        df["b"] = dda
        df["c"] = dda
        df.loc[[False, True], "b"] = 100
        result = df.loc[[1], :]
        expected = DataFrame({"a": ["b"], "b": [100], "c": [2]}, index=[1])
        tm.assert_frame_equal(result, expected)
    finally:
        pd.set_option("compute.use_numexpr", olduse)

