import os

def test_write_roundtrip(realfile, mmap, rate, channels, dt_str, tmpdir):
    dtype = np.dtype(dt_str)
    if realfile:
        tmpfile = str(tmpdir.join(str(threading.get_native_id()), 'temp.wav'))
        os.makedirs(os.path.dirname(tmpfile), exist_ok=True)
    else:
        tmpfile = BytesIO()
    data = np.random.rand(100, channels)
    if channels == 1:
        data = data[:, 0]
    if dtype.kind == 'f':
        # The range of the float type should be in [-1, 1]
        data = data.astype(dtype)
    else:
        data = (data*128).astype(dtype)

    wavfile.write(tmpfile, rate, data)

    rate2, data2 = wavfile.read(tmpfile, mmap=mmap)

    assert_equal(rate, rate2)
    assert_(data2.dtype.byteorder in ('<', '=', '|'), msg=data2.dtype)
    assert_array_equal(data, data2)
    # also test writing (gh-12176)
    if realfile:
        data2[0] = 0
    else:
        with pytest.raises(ValueError, match='read-only'):
            data2[0] = 0

