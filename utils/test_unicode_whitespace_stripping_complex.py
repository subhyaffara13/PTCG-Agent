
def test_unicode_whitespace_stripping_complex(dtype):
    # Complex has a few extra cases since it has two components and
    # parentheses
    line = " 1 , 2+3j , ( 4+5j ), ( 6+-7j )  , 8j , ( 9j ) \n"
    data = [line, line.replace(" ", "\u202F")]
    res = np.loadtxt(data, dtype=dtype, delimiter=',')
    assert_array_equal(res, np.array([[1, 2 + 3j, 4 + 5j, 6 - 7j, 8j, 9j]] * 2))

