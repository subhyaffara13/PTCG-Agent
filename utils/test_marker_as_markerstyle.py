
def test_marker_as_markerstyle():
    fix, ax = plt.subplots()
    m = mmarkers.MarkerStyle('o')
    ax.plot([1, 2, 3], [3, 2, 1], marker=m)
    ax.scatter([1, 2, 3], [4, 3, 2], marker=m)
    ax.errorbar([1, 2, 3], [5, 4, 3], marker=m)


def test_marker_as_markerstyle():
    fig, ax = plt.subplots()
    line, = ax.plot([2, 4, 3], marker=MarkerStyle("D"))
    fig.canvas.draw()
    assert line.get_marker() == "D"

    # continue with smoke tests:
    line.set_marker("s")
    fig.canvas.draw()
    line.set_marker(MarkerStyle("o"))
    fig.canvas.draw()
    # test Path roundtrip
    triangle1 = Path._create_closed([[-1, -1], [1, -1], [0, 2]])
    line2, = ax.plot([1, 3, 2], marker=MarkerStyle(triangle1), ms=22)
    line3, = ax.plot([0, 2, 1], marker=triangle1, ms=22)

    assert_array_equal(line2.get_marker().vertices, triangle1.vertices)
    assert_array_equal(line3.get_marker().vertices, triangle1.vertices)

