
def test_negative_step(slice_test_grouped):
    # Test for error on negative slice step

    with pytest.raises(ValueError, match="Invalid step"):
        slice_test_grouped.nth(slice(None, None, -1))

