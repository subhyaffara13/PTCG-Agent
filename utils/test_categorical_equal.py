
def test_categorical_equal(c):
    c = Categorical([1, 2, 3, 4], categories=c)
    tm.assert_categorical_equal(c, c)

