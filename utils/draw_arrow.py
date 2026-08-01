
def draw_arrow(surf, color, posn, direction: int):
    x, y = posn
    if direction == DIR_UP:
        pointlist = ((x - 29, y + 30), (x + 30, y + 30), (x + 1, y - 29), (x, y - 29))
    elif direction == DIR_DOWN:
        pointlist = ((x - 29, y - 29), (x + 30, y - 29), (x + 1, y + 30), (x, y + 30))
    elif direction == DIR_LEFT:
        pointlist = ((x + 30, y - 29), (x + 30, y + 30), (x - 29, y + 1), (x - 29, y))
    else:
        pointlist = ((x - 29, y - 29), (x - 29, y + 30), (x + 30, y + 1), (x + 30, y))
    pg.draw.polygon(surf, color, pointlist)


def draw_arrow(ax, t, r):
    ax.annotate('', xy=(0.5, 0.5 + r), xytext=(0.5, 0.5), size=30,
                arrowprops=dict(arrowstyle=t,
                                fc="b", ec='k'))

