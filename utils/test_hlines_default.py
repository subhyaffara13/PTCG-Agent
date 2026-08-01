
def test_hlines_default():
    fig, ax = plt.subplots()
    with mpl.rc_context({'lines.color': 'red'}):
        lines = ax.hlines(0.5, 0, 1)
        assert mpl.colors.same_color(lines.get_color(), 'red')

