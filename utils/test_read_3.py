
def test_read_3():
    # Little-endian float
    for mmap in [False, True]:
        filename = 'test-44100Hz-2ch-32bit-float-le.wav'
        rate, data = wavfile.read(datafile(filename), mmap=mmap)

        assert_equal(rate, 44100)
        assert_(np.issubdtype(data.dtype, np.float32))
        assert_equal(data.shape, (441, 2))

        del data

