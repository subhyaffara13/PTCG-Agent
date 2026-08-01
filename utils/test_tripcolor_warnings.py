
def test_tripcolor_warnings():
    x = [-1, 0, 1, 0]
    y = [0, -1, 0, 1]
    c = [0.4, 0.5]
    fig, ax = plt.subplots()
    # facecolors takes precedence over c
    with pytest.warns(UserWarning, match="Positional parameter c .*no effect"):
        ax.tripcolor(x, y, c, facecolors=c)
    with pytest.warns(UserWarning, match="Positional parameter c .*no effect"):
        ax.tripcolor(x, y, 'interpreted as c', facecolors=c)

