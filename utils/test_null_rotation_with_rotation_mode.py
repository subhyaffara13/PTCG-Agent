
def test_null_rotation_with_rotation_mode(ha, va):
    fig, ax = plt.subplots()
    kw = dict(rotation=0, va=va, ha=ha)
    t0 = ax.text(.5, .5, 'test', rotation_mode='anchor', **kw)
    t1 = ax.text(.5, .5, 'test', rotation_mode='default', **kw)
    fig.canvas.draw()
    assert_almost_equal(t0.get_window_extent(fig.canvas.renderer).get_points(),
                        t1.get_window_extent(fig.canvas.renderer).get_points())

