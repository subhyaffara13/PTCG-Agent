
def test_text_3d(fig_test, fig_ref):
    ax = fig_ref.add_subplot(projection="3d")
    txt = Text(0.5, 0.5, r'Foo bar $\int$')
    art3d.text_2d_to_3d(txt, z=1)
    ax.add_artist(txt)
    assert txt.get_position_3d() == (0.5, 0.5, 1)

    ax = fig_test.add_subplot(projection="3d")
    t3d = art3d.Text3D(0.5, 0.5, 1, r'Foo bar $\int$')
    ax.add_artist(t3d)
    assert t3d.get_position_3d() == (0.5, 0.5, 1)

