
def test_draw_single_lines_from_Nx1():
    # Smoke test for GH#23459
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot([[0], [1]], [[0], [1]], [[0], [1]])

