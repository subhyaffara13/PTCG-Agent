
def test_zipfian_distribution_wrapper():
    # Regression test for gh-23678: calling the cdf method at the end
    # point of the Zipfian distribution would generate a warning.
    Zipfian = stats.make_distribution(stats.zipfian)
    zdist = Zipfian(a=0.75, n=15)
    # This should not generate any warnings.
    assert_equal(zdist.cdf(15), 1.0)

