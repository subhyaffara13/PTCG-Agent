
def test_axline_transaxes_panzoom(fig_test, fig_ref):
    # test that it is robust against pan/zoom and
    # figure resize after plotting
    ax = fig_test.subplots()
    ax.set(xlim=(-1, 1), ylim=(-1, 1))
    ax.axline((0, 0), slope=1, transform=ax.transAxes)
    ax.axline((0.5, 0.5), slope=2, color='C1', transform=ax.transAxes)
    ax.axline((0.5, 0.5), slope=0, color='C2', transform=ax.transAxes)
    ax.set(xlim=(0, 5), ylim=(0, 10))
    fig_test.set_size_inches(3, 3)

    ax = fig_ref.subplots()
    ax.set(xlim=(0, 5), ylim=(0, 10))
    fig_ref.set_size_inches(3, 3)
    ax.plot([0, 5], [0, 5])
    ax.plot([0, 5], [0, 10], color='C1')
    ax.plot([0, 5], [5, 5], color='C2')

