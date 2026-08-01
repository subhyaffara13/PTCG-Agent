
def test_axline(fig_test, fig_ref):
    ax = fig_test.subplots()
    ax.set(xlim=(-1, 1), ylim=(-1, 1))
    ax.axline((0, 0), (1, 1))
    ax.axline((0, 0), (1, 0), color='C1')
    ax.axline((0, 0.5), (1, 0.5), color='C2')
    # slopes
    ax.axline((-0.7, -0.5), slope=0, color='C3')
    ax.axline((1, -0.5), slope=-0.5, color='C4')
    ax.axline((-0.5, 1), slope=float('inf'), color='C5')

    ax = fig_ref.subplots()
    ax.set(xlim=(-1, 1), ylim=(-1, 1))
    ax.plot([-1, 1], [-1, 1])
    ax.axhline(0, color='C1')
    ax.axhline(0.5, color='C2')
    # slopes
    ax.axhline(-0.5, color='C3')
    ax.plot([-1, 1], [0.5, -0.5], color='C4')
    ax.axvline(-0.5, color='C5')

