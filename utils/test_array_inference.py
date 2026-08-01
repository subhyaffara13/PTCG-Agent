
def test_array_inference(data, expected):
    result = pd.array(data)
    tm.assert_equal(result, expected)

