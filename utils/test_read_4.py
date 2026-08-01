
def test_read_4():
    # Contains unsupported 'PEAK' chunk
    for mmap in [False, True]:
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                "Chunk .non-data. not understood, skipping it",
                wavfile.WavFileWarning
            )
            filename = 'test-48000Hz-2ch-64bit-float-le-wavex.wav'
            rate, data = wavfile.read(datafile(filename), mmap=mmap)

        assert_equal(rate, 48000)
        assert_(np.issubdtype(data.dtype, np.float64))
        assert_equal(data.shape, (480, 2))

        del data

