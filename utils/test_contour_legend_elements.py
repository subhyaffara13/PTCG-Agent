
def test_contour_legend_elements():
    x, y = np.mgrid[1:10, 1:10]
    h = x * y
    colors = ['blue', '#00FF00', 'red']

    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    cs = ax.contour(x, y, h, levels=[10, 30, 50], colors=colors, extend='both')

    artists, labels = cs.legend_elements()
    assert labels == ['$x = 10.0$', '$x = 30.0$', '$x = 50.0$']
    assert all(isinstance(a, mpl.lines.Line2D) for a in artists)
    assert all(same_color(a.get_color(), c)
               for a, c in zip(artists, colors))


def test_contour_legend_elements():
    x = np.arange(1, 10)
    y = x.reshape(-1, 1)
    h = x * y

    colors = ['blue', '#00FF00', 'red']
    cs = plt.contour(h, levels=[10, 30, 50],
                     colors=colors,
                     extend='both')
    artists, labels = cs.legend_elements()
    assert labels == ['$x = 10.0$', '$x = 30.0$', '$x = 50.0$']
    assert all(isinstance(a, mpl.lines.Line2D) for a in artists)
    assert all(same_color(a.get_color(), c)
               for a, c in zip(artists, colors))

