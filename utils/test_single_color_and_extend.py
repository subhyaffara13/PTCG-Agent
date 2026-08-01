
def test_single_color_and_extend(color, extend):
    z = [[0, 1], [1, 2]]

    _, ax = plt.subplots()
    levels = [0.5, 0.75, 1, 1.25, 1.5]
    cs = ax.contour(z, levels=levels, colors=color, extend=extend)
    for c in cs.get_edgecolors():
        assert same_color(c, color)

