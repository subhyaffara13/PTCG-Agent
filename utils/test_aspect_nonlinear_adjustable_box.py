
def test_aspect_nonlinear_adjustable_box():
    fig = plt.figure(figsize=(10, 10))  # Square.

    ax = fig.add_subplot()
    ax.plot([.4, .6], [.4, .6])  # Set minpos to keep logit happy.
    ax.set(xscale="log", xlim=(1, 10),
           yscale="logit", ylim=(1/11, 1/1001),
           aspect=1, adjustable="box")
    ax.margins(0)
    pos = fig.transFigure.transform_bbox(ax.get_position())
    assert pos.height / pos.width == pytest.approx(2)

