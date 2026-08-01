
def test_read_2():
    # 8-bit unsigned PCM
    for mmap in [False, True]:
        filename = 'test-8000Hz-le-2ch-1byteu.wav'
        rate, data = wavfile.read(datafile(filename), mmap=mmap)

        assert_equal(rate, 8000)
        assert_(np.issubdtype(data.dtype, np.uint8))
        assert_equal(data.shape, (800, 2))

        del data

