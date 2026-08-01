
def test_stats_shapes_argcheck():
    # stats method was failing for vector shapes if some of the values
    # were outside of the allowed range, see gh-2678
    mv3 = stats.invgamma.stats([0.0, 0.5, 1.0], 1, 0.5)  # 0 is not a legal `a`
    mv2 = stats.invgamma.stats([0.5, 1.0], 1, 0.5)
    mv2_augmented = tuple(np.r_[np.nan, _] for _ in mv2)
    assert_equal(mv2_augmented, mv3)

    # -1 is not a legal shape parameter
    mv3 = stats.lognorm.stats([2, 2.4, -1])
    mv2 = stats.lognorm.stats([2, 2.4])
    mv2_augmented = tuple(np.r_[_, np.nan] for _ in mv2)
    assert_equal(mv2_augmented, mv3)

