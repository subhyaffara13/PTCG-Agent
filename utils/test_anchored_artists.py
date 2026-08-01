
def test_anchored_artists():
    fig, ax = plt.subplots(figsize=(3, 3))
    ada = AnchoredDrawingArea(40, 20, 0, 0, loc='upper right', pad=0.,
                              frameon=False)
    p1 = Circle((10, 10), 10)
    ada.drawing_area.add_artist(p1)
    p2 = Circle((30, 10), 5, fc="r")
    ada.drawing_area.add_artist(p2)
    ax.add_artist(ada)

    box = AnchoredAuxTransformBox(ax.transData, loc='upper left')
    el = Ellipse((0, 0), width=0.1, height=0.4, angle=30, color='cyan')
    box.drawing_area.add_artist(el)
    ax.add_artist(box)

    asb = AnchoredSizeBar(ax.transData, 0.2, r"0.2 units", loc='lower right',
                          pad=0.3, borderpad=0.4, sep=4, fill_bar=True,
                          frameon=False, label_top=True, prop={'size': 20},
                          size_vertical=0.05, color='green')
    ax.add_artist(asb)

