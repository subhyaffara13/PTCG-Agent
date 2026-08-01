
def test_too_many_positional():
    # the second argument is positional but can be passed as keyword.
    with pytest.raises(TypeError,
            match="takes from 2 to 3 positional arguments but 4 were given"):
        func(1, 2, 3, 4)

