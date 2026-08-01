
def test_td_construction_with_np_dtypes(npdtype, item):
    # GH#8757: test construction with np dtypes
    pykwarg, npkwarg = item
    expected = np.timedelta64(1, npkwarg).astype("m8[us]").view("i8")
    assert Timedelta(**{pykwarg: npdtype(1)})._value == expected

