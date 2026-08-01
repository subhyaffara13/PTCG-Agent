
def test_gh1320_regression():
    # Check that the first example from gh-1320 now works.
    c = 2.62
    stats.genextreme.ppf(0.5, np.array([[c], [c + 0.5]]))

