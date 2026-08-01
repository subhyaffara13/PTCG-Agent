
def test_fancyarrow_shape_error():
    with pytest.raises(ValueError, match="Got unknown shape: 'foo'"):
        FancyArrow(0, 0, 0.2, 0.2, shape='foo')

