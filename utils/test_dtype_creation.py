
def test_dtype_creation():
    hashes = set()
    dt = StringDType()
    assert not hasattr(dt, "na_object") and dt.coerce is True
    hashes.add(hash(dt))

    dt = StringDType(na_object=None)
    assert dt.na_object is None and dt.coerce is True
    hashes.add(hash(dt))

    dt = StringDType(coerce=False)
    assert not hasattr(dt, "na_object") and dt.coerce is False
    hashes.add(hash(dt))

    dt = StringDType(na_object=None, coerce=False)
    assert dt.na_object is None and dt.coerce is False
    hashes.add(hash(dt))

    assert len(hashes) == 4

    dt = np.dtype("T")
    assert dt == StringDType()
    assert dt.kind == "T"
    assert dt.char == "T"

    hashes.add(hash(dt))
    assert len(hashes) == 4

