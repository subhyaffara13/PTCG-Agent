
def test_const_name(func, selector, expected):
    if isinstance(func, str):
        pytest.skip(func)
    text = func(selector)
    assert text == expected

