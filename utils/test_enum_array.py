
def test_enum_array():
    from sys import byteorder

    e = "<" if byteorder == "little" else ">"

    arr = m.create_enum_array(3)
    dtype = arr.dtype
    assert dtype == np.dtype([("e1", e + "i8"), ("e2", "u1")])
    assert m.print_enum_array(arr) == ["e1=A,e2=X", "e1=B,e2=Y", "e1=A,e2=X"]
    assert arr["e1"].tolist() == [-1, 1, -1]
    assert arr["e2"].tolist() == [1, 2, 1]
    assert m.create_enum_array(0).dtype == dtype

