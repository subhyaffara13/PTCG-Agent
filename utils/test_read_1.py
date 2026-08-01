
def test_read_1():
    # 32-bit PCM (which uses extensible format)
    for mmap in [False, True]:
        filename = 'test-44100Hz-le-1ch-4bytes.wav'
        rate, data = wavfile.read(datafile(filename), mmap=mmap)

        assert_equal(rate, 44100)
        assert_(np.issubdtype(data.dtype, np.int32))
        assert_equal(data.shape, (4410,))

        del data

