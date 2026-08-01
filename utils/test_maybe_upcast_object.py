
def test_maybe_upcast_object(val, string_storage):
    # GH#36712
    pa = pytest.importorskip("pyarrow")

    with pd.option_context("mode.string_storage", string_storage):
        arr = np.array(["a", "b", val], dtype=np.object_)
        result = _maybe_upcast(arr, use_dtype_backend=True)

        if string_storage == "python":
            exp_val = "c" if val == "c" else NA
            expected = pd.array(["a", "b", exp_val], dtype=pd.StringDtype())
        else:
            exp_val = "c" if val == "c" else None
            expected = ArrowStringArray(pa.array(["a", "b", exp_val]))
        tm.assert_extension_array_equal(result, expected)

