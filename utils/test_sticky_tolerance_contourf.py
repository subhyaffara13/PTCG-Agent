
def test_sticky_tolerance_contourf():
    fig, ax = plt.subplots()

    x = y = [14496.71, 14496.75]
    data = [[0, 1], [2, 3]]

    ax.contourf(x, y, data)

