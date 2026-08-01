
def test_axes_handles_same_functions(fig_ref, fig_test):
    # prove that cax and cb.ax are functionally the same
    for nn, fig in enumerate([fig_ref, fig_test]):
        ax = fig.add_subplot()
        pc = ax.pcolormesh(np.ones(300).reshape(10, 30))
        cax = fig.add_axes((0.9, 0.1, 0.03, 0.8))
        cb = fig.colorbar(pc, cax=cax)
        if nn == 0:
            caxx = cax
        else:
            caxx = cb.ax
        caxx.set_yticks(np.arange(0, 20))
        caxx.set_yscale('log')
        caxx.set_position([0.92, 0.1, 0.02, 0.7])

