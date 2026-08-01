
def test_24_bit_odd_size_with_pad():
    # 24-bit, 3 B container, 3 channels, 5 samples, 45 B data chunk
    # Should not raise any warnings about the data chunk pad byte
    filename = 'test-8000Hz-le-3ch-5S-24bit.wav'
    rate, data = wavfile.read(datafile(filename), mmap=False)

    assert_equal(rate, 8000)
    assert_(np.issubdtype(data.dtype, np.int32))
    assert_equal(data.shape, (5, 3))

    # All LSBytes should be 0
    assert_equal(data & 0xff, 0)

    # Hand-made max/min samples under different conventions:
    #                      2**(N-1)     2**(N-1)-1     LSB
    assert_equal(data, [[-0x8000_0000, -0x7fff_ff00, -0x200],
                        [-0x4000_0000, -0x3fff_ff00, -0x100],
                        [+0x0000_0000, +0x0000_0000, +0x000],
                        [+0x4000_0000, +0x3fff_ff00, +0x100],
                        [+0x7fff_ff00, +0x7fff_ff00, +0x200]])

