
def test_from_product_invalid_input(invalid_input):
    msg = r"Input must be a list / sequence of iterables|Input must be list-like"
    with pytest.raises(TypeError, match=msg):
        MultiIndex.from_product(iterables=invalid_input)

