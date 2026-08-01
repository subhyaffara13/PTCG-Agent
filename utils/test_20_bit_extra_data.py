
def test_20_bit_extra_data():
    # 20-bit, 3 B container, 1 channel, 10 samples, 30 B data chunk
    # with extra data filling container beyond the bit depth
    filename = 'test-1234Hz-le-1ch-10S-20bit-extra.wav'
    rate, data = wavfile.read(datafile(filename), mmap=False)

    assert_equal(rate, 1234)
    assert_(np.issubdtype(data.dtype, np.int32))
    assert_equal(data.shape, (10,))

    # All LSBytes should still be 0, because 3 B container in 4 B dtype
    assert_equal(data & 0xff, 0)

    # But it should load the data beyond 20 bits
    assert_((data & 0xf00).any())

    # Full-scale positive/negative samples, then being halved each time
    assert_equal(data, [+0x7ffff000,       # +full-scale 20-bit
                        -0x7ffff000,       # -full-scale 20-bit
                        +0x7ffff000 >> 1,  # +1/2
                        -0x7ffff000 >> 1,  # -1/2
                        +0x7ffff000 >> 2,  # +1/4
                        -0x7ffff000 >> 2,  # -1/4
                        +0x7ffff000 >> 3,  # +1/8
                        -0x7ffff000 >> 3,  # -1/8
                        +0x7ffff000 >> 4,  # +1/16
                        -0x7ffff000 >> 4,  # -1/16
                        ])

