
def test_axline_transaxes(fig_test, fig_ref):
    ax = fig_test.subplots()
    ax.set(xlim=(-1, 1), ylim=(-1, 1))
    ax.axline((0, 0), slope=1, transform=ax.transAxes)
    ax.axline((1, 0.5), slope=1, color='C1', transform=ax.transAxes)
    ax.axline((0.5, 0.5), slope=0, color='C2', transform=ax.transAxes)
    ax.axline((0.5, 0), (0.5, 1), color='C3', transform=ax.transAxes)

    ax = fig_ref.subplots()
    ax.set(xlim=(-1, 1), ylim=(-1, 1))
    ax.plot([-1, 1], [-1, 1])
    ax.plot([0, 1], [-1, 0], color='C1')
    ax.plot([-1, 1], [0, 0], color='C2')
    ax.plot([0, 0], [-1, 1], color='C3')

