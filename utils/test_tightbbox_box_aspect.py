
def test_tightbbox_box_aspect():
    fig = plt.figure()
    gs = fig.add_gridspec(1, 2)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1], projection='3d')
    ax1.set_box_aspect(.5)
    ax2.set_box_aspect((2, 1, 1))

