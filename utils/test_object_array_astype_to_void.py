
def test_object_array_astype_to_void():
    # This is different to `test_array_astype_to_void` as object arrays
    # are inspected.  The default void is "V8" (8 is the length of double)
    arr = np.array([], dtype="O").astype("V")
    assert arr.dtype == "V8"

