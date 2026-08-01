
def test_object_cleanup_on_read_error():
    sentinel = object()
    already_read = 0

    def conv(x):
        nonlocal already_read
        if already_read > 4999:
            raise ValueError("failed half-way through!")
        already_read += 1
        return sentinel

    txt = StringIO("x\n" * 10000)

    with pytest.raises(ValueError, match="at row 5000, column 1"):
        np.loadtxt(txt, dtype=object, converters={0: conv})

    assert sys.getrefcount(sentinel) == 2

