
def test_assert_numpy_array_equal_class_mismatch(a, b, klass1, klass2):
    msg = f"""numpy array are different

numpy array classes are different
\\[left\\]:  {klass1}
\\[right\\]: {klass2}"""

    with pytest.raises(AssertionError, match=msg):
        tm.assert_numpy_array_equal(a, b)

