
def test_write_roundtrip_rf64(tmpdir):
    dtype = np.dtype("<i8")
    tmpfile = str(tmpdir.join('temp.wav'))
    rate = 44100
    data = np.random.randint(0, 127, (2**29,)).astype(dtype)

    wavfile.write(tmpfile, rate, data)

    rate2, data2 = wavfile.read(tmpfile, mmap=True)

    assert_equal(rate, rate2)
    msg = f"{data2.dtype} byteorder not in ('<', '=', '|')"
    assert data2.dtype.byteorder in ('<', '=', '|'), msg
    assert_array_equal(data, data2)
    # also test writing (gh-12176)
    data2[0] = 0

