
def test_multi_color_hatch():
    fig, ax = plt.subplots()

    rects = ax.bar(range(5), range(1, 6))
    for i, rect in enumerate(rects):
        rect.set_facecolor('none')
        rect.set_edgecolor(f'C{i}')
        rect.set_hatch('/')

    ax.autoscale_view()
    ax.autoscale(False)

    for i in range(5):
        with mpl.style.context({'hatch.color': f'C{i}'}):
            r = Rectangle((i - .8 / 2, 5), .8, 1, hatch='//', fc='none')
        ax.add_patch(r)

