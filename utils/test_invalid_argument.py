
def test_invalid_argument(slice_test_grouped):
    # Test for error on invalid argument

    with pytest.raises(TypeError, match="Invalid index"):
        slice_test_grouped.nth(3.14)

