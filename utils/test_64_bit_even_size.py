
def test_64_bit_even_size():
    # 64-bit, 8 B container, 3 channels, 5 samples, 120 B data chunk
    for mmap in [False, True]:
        filename = 'test-8000Hz-le-3ch-5S-64bit.wav'
        rate, data = wavfile.read(datafile(filename), mmap=mmap)

        assert_equal(rate, 8000)
        assert_(np.issubdtype(data.dtype, np.int64))
        assert_equal(data.shape, (5, 3))

        # Hand-made max/min samples under different conventions:
        #            Fixed-point 2**(N-1)    Full-scale 2**(N-1)-1   LSB
        correct = [[-0x8000_0000_0000_0000, -0x7fff_ffff_ffff_ffff, -0x2],
                   [-0x4000_0000_0000_0000, -0x3fff_ffff_ffff_ffff, -0x1],
                   [+0x0000_0000_0000_0000, +0x0000_0000_0000_0000, +0x0],
                   [+0x4000_0000_0000_0000, +0x3fff_ffff_ffff_ffff, +0x1],
                   [+0x7fff_ffff_ffff_ffff, +0x7fff_ffff_ffff_ffff, +0x2]]
        #              ^ clipped

        assert_equal(data, correct)

        del data

