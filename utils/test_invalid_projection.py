
def test_invalid_projection():
    with pytest.raises(ValueError,
                       match=r"'aitof' is not a valid value for projection\. "
                             r"Did you mean: 'aitoff'\?"):
        plt.subplots(subplot_kw={'projection': 'aitof'})

