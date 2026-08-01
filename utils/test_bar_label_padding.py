
def test_bar_label_padding():
    """Test that bar_label accepts both float and array-like padding."""
    ax = plt.gca()
    xs, heights = [1, 2], [3, 4]
    rects = ax.bar(xs, heights)
    labels1 = ax.bar_label(rects, padding=5)  # test float value
    assert labels1[0].xyann[1] == 5
    assert labels1[1].xyann[1] == 5

    labels2 = ax.bar_label(rects, padding=[2, 8])  # test array-like values
    assert labels2[0].xyann[1] == 2
    assert labels2[1].xyann[1] == 8

    with pytest.raises(ValueError, match="padding must be of length"):
        ax.bar_label(rects, padding=[1, 2, 3])

