
def test_hdfstore_strides(temp_hdfstore):
    # GH22073
    df = DataFrame({"a": [1, 2, 3, 4], "b": [5, 6, 7, 8]})
    temp_hdfstore.put("df", df)
    assert df["a"].values.strides == temp_hdfstore["df"]["a"].values.strides

