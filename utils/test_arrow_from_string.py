
def test_arrow_from_string(using_infer_string):
    # not roundtrip,  but starting with pyarrow table without pandas metadata
    pa = pytest.importorskip("pyarrow")
    table = pa.table({"a": pa.array(["a", "b", None], type=pa.string())})

    result = table.to_pandas()

    if not using_infer_string:
        if pa_version_under19p0:
            expected = pd.DataFrame({"a": ["a", "b", None]}, dtype="object")
        else:
            expected = pd.DataFrame(
                {"a": ["a", "b", None]}, dtype=pd.StringDtype(na_value=np.nan)
            )
    elif pa_version_under19p0:
        expected = pd.DataFrame({"a": ["a", "b", None]}, dtype="object")
    else:
        expected = pd.DataFrame({"a": ["a", "b", None]}, dtype="str")
    tm.assert_frame_equal(result, expected)

