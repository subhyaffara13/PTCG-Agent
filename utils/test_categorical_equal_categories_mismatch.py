
def test_categorical_equal_categories_mismatch():
    msg = """Categorical\\.categories are different

Categorical\\.categories values are different \\(25\\.0 %\\)
\\[left\\]:  Index\\(\\[1, 2, 3, 4\\], dtype='int64'\\)
\\[right\\]: Index\\(\\[1, 2, 3, 5\\], dtype='int64'\\)"""

    c1 = Categorical([1, 2, 3, 4])
    c2 = Categorical([1, 2, 3, 5])

    with pytest.raises(AssertionError, match=msg):
        tm.assert_categorical_equal(c1, c2)

