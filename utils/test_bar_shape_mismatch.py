
def test_bar_shape_mismatch():
    x = ["foo", "bar"]
    height = [1, 2, 3]
    error_message = (
        r"Mismatch is between 'x' with shape \(2,\) and 'height' with shape \(3,\)"
    )
    with pytest.raises(ValueError, match=error_message):
        plt.bar(x, height)

