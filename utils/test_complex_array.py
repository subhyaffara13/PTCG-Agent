
def test_complex_array():
    from sys import byteorder

    e = "<" if byteorder == "little" else ">"

    arr = m.create_complex_array(3)
    dtype = arr.dtype
    assert dtype == np.dtype([("cflt", e + "c8"), ("cdbl", e + "c16")])
    assert m.print_complex_array(arr) == [
        "c:(0,0.25),(0.5,0.75)",
        "c:(1,1.25),(1.5,1.75)",
        "c:(2,2.25),(2.5,2.75)",
    ]
    assert arr["cflt"].tolist() == [0.0 + 0.25j, 1.0 + 1.25j, 2.0 + 2.25j]
    assert arr["cdbl"].tolist() == [0.5 + 0.75j, 1.5 + 1.75j, 2.5 + 2.75j]
    assert m.create_complex_array(0).dtype == dtype

