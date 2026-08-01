
def test_astype_copy_false():
    orig_dt = StringDType()
    arr = np.array(["hello", "world"], dtype=StringDType())
    assert not arr.astype(StringDType(coerce=False), copy=False).dtype.coerce

    assert arr.astype(orig_dt, copy=False).dtype is orig_dt

