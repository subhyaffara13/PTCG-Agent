
def test_exception_message_bad_values(dtype):
    txt = StringIO("1,2\n3,XXX\n5,6")
    msg = f"could not convert string 'XXX' to {dtype} at row 1, column 2"
    with pytest.raises(ValueError, match=msg):
        np.loadtxt(txt, dtype=dtype, delimiter=",")

