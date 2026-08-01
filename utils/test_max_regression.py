
def test_max_regression():
    arr = np.array(['y', 'y', 'z'], dtype="T")
    assert arr.max() == 'z'

