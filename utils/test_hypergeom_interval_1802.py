
def test_hypergeom_interval_1802():
    # these two had endless loops
    assert_equal(stats.hypergeom.interval(.95, 187601, 43192, 757),
                 (152.0, 197.0))
    assert_equal(stats.hypergeom.interval(.945, 187601, 43192, 757),
                 (152.0, 197.0))
    # this was working also before
    assert_equal(stats.hypergeom.interval(.94, 187601, 43192, 757),
                 (153.0, 196.0))

    # degenerate case .a == .b
    assert_equal(stats.hypergeom.ppf(0.02, 100, 100, 8), 8)
    assert_equal(stats.hypergeom.ppf(1, 100, 100, 8), 8)

