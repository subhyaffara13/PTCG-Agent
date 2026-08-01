
def test_bar_label_fmt_error():
    ax = plt.gca()
    rects = ax.bar([1, 2], [3, -4])
    with pytest.raises(TypeError, match='str or callable'):
        _ = ax.bar_label(rects, fmt=10)

