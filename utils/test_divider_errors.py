
def test_divider_errors(anchor, error, message):
    fig = plt.figure()
    with pytest.raises(error, match=message):
        Divider(fig, [0, 0, 1, 1], [Size.Fixed(1)], [Size.Fixed(1)],
                anchor=anchor)

