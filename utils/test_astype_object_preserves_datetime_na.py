
def test_astype_object_preserves_datetime_na(from_type):
    arr = np.array([from_type("NaT", "ns")])
    result = astype_array(arr, dtype=np.dtype("object"))

    assert isna(result)[0]

