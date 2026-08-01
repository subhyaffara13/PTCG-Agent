
def test_rect():
    fig, ax = plt.subplots(layout='constrained')
    fig.get_layout_engine().set(rect=[0, 0, 0.5, 0.5])
    fig.draw_without_rendering()
    ppos = ax.get_position()
    assert ppos.x1 < 0.5
    assert ppos.y1 < 0.5

    fig, ax = plt.subplots(layout='constrained')
    fig.get_layout_engine().set(rect=[0.2, 0.2, 0.3, 0.3])
    fig.draw_without_rendering()
    ppos = ax.get_position()
    assert ppos.x1 < 0.5
    assert ppos.y1 < 0.5
    assert ppos.x0 > 0.2
    assert ppos.y0 > 0.2

