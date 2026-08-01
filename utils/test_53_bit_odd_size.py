
def test_53_bit_odd_size():
    # 53-bit, 7 B container, 3 channels, 5 samples, 105 B data chunk + pad
    filename = 'test-8000Hz-le-3ch-5S-53bit.wav'
    rate, data = wavfile.read(datafile(filename), mmap=False)

    assert_equal(rate, 8000)
    assert_(np.issubdtype(data.dtype, np.int64))
    assert_equal(data.shape, (5, 3))

    # 11 LSBits should be 0
    assert_equal(data & 0x7ff, 0)

    # Hand-made max/min samples under different conventions:
    #            Fixed-point 2**(N-1)    Full-scale 2**(N-1)-1    LSB
    correct = [[-0x8000_0000_0000_0000, -0x7fff_ffff_ffff_f800, -0x1000],
               [-0x4000_0000_0000_0000, -0x3fff_ffff_ffff_f800, -0x0800],
               [+0x0000_0000_0000_0000, +0x0000_0000_0000_0000, +0x0000],
               [+0x4000_0000_0000_0000, +0x3fff_ffff_ffff_f800, +0x0800],
               [+0x7fff_ffff_ffff_f800, +0x7fff_ffff_ffff_f800, +0x1000]]
    #              ^ clipped

    assert_equal(data, correct)

