
def test_rational2_uses_new_dtype_api():
    # ``rational2`` provides its own ``common_dtype`` slot (which the
    # legacy ``rational`` cannot), and that slot rejects floats.
    assert np.result_type(rational, 1.0) == np.float64
    with pytest.raises(TypeError,
            match=r".* no common DType exists for the given inputs"):
        np.result_type(rational2, 1.0)

