
def test_embedded_null_string_like_casts(dtype):
    strings = ["a\0b", "\0leading", "multi\0null\0inside"]
    arr = np.array(strings, dtype="T")
    roundtripped = arr.astype(dtype).astype("T")

    assert roundtripped.tolist() == strings

