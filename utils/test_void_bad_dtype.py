
def test_void_bad_dtype():
    with pytest.raises(TypeError,
            match="void: descr must be a `void.*int64"):
        np.void(4, dtype="i8")

    # Subarray dtype (with shape `(4,)` is rejected):
    with pytest.raises(TypeError,
            match=r"void: descr must be a `void.*\(4,\)"):
        np.void(4, dtype="4i")

