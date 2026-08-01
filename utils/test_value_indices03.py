
def test_value_indices03(xp):
    "Test different input array shapes, from 1-D to 4-D"
    for shape in [(36,), (18, 2), (3, 3, 4), (3, 3, 2, 2)]:
        a = np.asarray((12*[1]+12*[2]+12*[3]), dtype=np.int32)
        a = np.reshape(a, shape)

        trueKeys = np.unique(a)
        a = xp.asarray(a)
        vi = ndimage.value_indices(a)
        assert list(vi.keys()) == list(trueKeys)
        for k in [int(x) for x in trueKeys]:
            trueNdx = xp.nonzero(a == k)
            assert len(vi[k]) == len(trueNdx)
            for vik, true_vik in zip(vi[k], trueNdx):
                xp_assert_equal(vik, true_vik)

