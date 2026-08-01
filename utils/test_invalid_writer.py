
def test_invalid_writer():
    # Note, this triggers for Animation.save as well, but this is a lighter test.
    with pytest.raises(ValueError,
                       match=r"'pllow' is not a valid value for writer\. "
                             r"Did you mean: 'pillow'\?"):
        animation.writers['pllow']

