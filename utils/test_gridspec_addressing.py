
def test_gridspec_addressing():
    fig = plt.figure()
    gs = fig.add_gridspec(3, 3)
    sp = fig.add_subplot(gs[0:, 1:])
    fig.draw_without_rendering()

