
def test_multiple_values():
    with pytest.raises(TypeError,
            match=r"given by name \('arg2'\) and position \(position 1\)"):
        func(1, 2, arg2=3)

