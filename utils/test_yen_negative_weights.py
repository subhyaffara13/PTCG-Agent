
def test_yen_negative_weights():
    distances = yen(
        directed_negative_weighted_G,
        source=2,
        sink=0,
        K=1,
    )
    assert_allclose(distances, [-2.])

