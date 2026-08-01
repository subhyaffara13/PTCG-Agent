
def test_apply_raw_mixed_type_frame(axis, engine):
    if engine == "numba":
        pytest.skip("isinstance check doesn't work with numba")

    def _assert_raw(x):
        assert isinstance(x, np.ndarray)
        assert x.ndim == 1

    # Mixed dtype (GH-32423)
    df = DataFrame(
        {
            "a": 1.0,
            "b": 2,
            "c": "foo",
            "float32": np.array([1.0] * 10, dtype="float32"),
            "int32": np.array([1] * 10, dtype="int32"),
        },
        index=np.arange(10),
    )
    df.apply(_assert_raw, axis=axis, engine=engine, raw=True)

