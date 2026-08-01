
def test_type_error():
    # Pass in a parameter not of type "set"
    raises(TypeError, lambda: Contains(2, None))

