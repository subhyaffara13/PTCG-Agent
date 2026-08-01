
def test_540_567():
    # test for nan returned in tickets 540, 567
    assert_almost_equal(stats.norm.cdf(-1.7624320982), 0.03899815971089126,
                        decimal=10, err_msg='test_540_567')
    assert_almost_equal(stats.norm.cdf(-1.7624320983), 0.038998159702449846,
                        decimal=10, err_msg='test_540_567')
    assert_almost_equal(stats.norm.cdf(1.38629436112, loc=0.950273420309,
                                       scale=0.204423758009),
                        0.98353464004309321,
                        decimal=10, err_msg='test_540_567')

