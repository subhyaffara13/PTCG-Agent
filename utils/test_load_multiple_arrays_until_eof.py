
def test_load_multiple_arrays_until_eof():
    f = BytesIO()
    np.save(f, 1)
    np.save(f, 2)
    f.seek(0)
    out1 = np.load(f)
    assert out1 == 1
    out2 = np.load(f)
    assert out2 == 2
    with pytest.raises(EOFError):
        np.load(f)

