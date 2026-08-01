
def test_sparse_dtype_subtype_must_be_numpy_dtype():
    # GH#53160
    msg = "SparseDtype subtype must be a numpy dtype"
    with pytest.raises(TypeError, match=msg):
        SparseDtype("category", fill_value="c")

