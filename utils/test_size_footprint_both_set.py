
def test_size_footprint_both_set(xp):
    # test for input validation, expect user warning when
    # size and footprint is set
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",
                                "ignoring size because footprint is set", UserWarning)
        arr = xp.asarray(np.random.random((10, 20, 30)))
        footprint = xp.asarray(np.ones((1, 1, 10), dtype=bool))
        ndimage.rank_filter(
            arr, 5, size=2, footprint=footprint
        )

