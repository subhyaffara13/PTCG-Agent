
def test_invalid_line_data():
    with pytest.raises(RuntimeError, match='x must be'):
        art3d.Line3D(0, [], [])
    with pytest.raises(RuntimeError, match='y must be'):
        art3d.Line3D([], 0, [])
    with pytest.raises(RuntimeError, match='z must be'):
        art3d.Line3D([], [], 0)

    line = art3d.Line3D([], [], [])
    with pytest.raises(RuntimeError, match='x must be'):
        line.set_data_3d(0, [], [])
    with pytest.raises(RuntimeError, match='y must be'):
        line.set_data_3d([], 0, [])
    with pytest.raises(RuntimeError, match='z must be'):
        line.set_data_3d([], [], 0)


def test_invalid_line_data():
    with pytest.raises(RuntimeError, match='xdata must be'):
        mlines.Line2D(0, [])
    with pytest.raises(RuntimeError, match='ydata must be'):
        mlines.Line2D([], 1)

    line = mlines.Line2D([], [])
    with pytest.raises(RuntimeError, match='x must be'):
        line.set_xdata(0)
    with pytest.raises(RuntimeError, match='y must be'):
        line.set_ydata(0)

