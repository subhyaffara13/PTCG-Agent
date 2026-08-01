
def test_wavfile_dtype_unsupported(tmpdir, dtype):
    tmpfile = str(tmpdir.join('temp.wav'))
    rng = np.random.default_rng(1234)
    data = rng.random((100, 5)).astype(dtype)
    rate = 8000
    with pytest.raises(ValueError, match="Unsupported"):
        wavfile.write(tmpfile, rate, data)

