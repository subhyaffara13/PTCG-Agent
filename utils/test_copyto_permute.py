
def test_copyto_permute():
    # test explicit overflow case
    pad = 500
    l = [True] * pad + [True, True, True, True]
    r = np.zeros(len(l) - pad)
    d = np.ones(len(l) - pad)
    mask = np.array(l)[pad:]
    np.copyto(r, d, where=mask[::-1])

    # test all permutation of possible masks, 9 should be sufficient for
    # current 4 byte unrolled code
    power = 9
    d = np.ones(power)
    for i in range(2**power):
        r = np.zeros(power)
        l = [(i & x) != 0 for x in range(power)]
        mask = np.array(l)
        np.copyto(r, d, where=mask)
        assert_array_equal(r == 1, l)
        assert_equal(r.sum(), sum(l))

        r = np.zeros(power)
        np.copyto(r, d, where=mask[::-1])
        assert_array_equal(r == 1, l[::-1])
        assert_equal(r.sum(), sum(l))

        r = np.zeros(power)
        np.copyto(r[::2], d[::2], where=mask[::2])
        assert_array_equal(r[::2] == 1, l[::2])
        assert_equal(r[::2].sum(), sum(l[::2]))

        r = np.zeros(power)
        np.copyto(r[::2], d[::2], where=mask[::-2])
        assert_array_equal(r[::2] == 1, l[::-2])
        assert_equal(r[::2].sum(), sum(l[::-2]))

        for c in [0xFF, 0x7F, 0x02, 0x10]:
            r = np.zeros(power)
            mask = np.array(l)
            imask = np.array(l).view(np.uint8)
            imask[mask != 0] = c
            np.copyto(r, d, where=mask)
            assert_array_equal(r == 1, l)
            assert_equal(r.sum(), sum(l))

    r = np.zeros(power)
    np.copyto(r, d, where=True)
    assert_equal(r.sum(), r.size)
    r = np.ones(power)
    d = np.zeros(power)
    np.copyto(r, d, where=False)
    assert_equal(r.sum(), r.size)

