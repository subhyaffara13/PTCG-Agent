
def test_compare_medians_ms():
    x = np.arange(7)
    y = x + 10
    assert_almost_equal(ms.compare_medians_ms(x, y), 0)

    y2 = np.linspace(0, 1, num=10)
    assert_almost_equal(ms.compare_medians_ms(x, y2), 0.017116406778)

