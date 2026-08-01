
def test_colorbar_change_lim_scale():
    fig, ax = plt.subplots(1, 2, constrained_layout=True)
    pc = ax[0].pcolormesh(np.arange(100).reshape(10, 10)+1)
    cb = fig.colorbar(pc, ax=ax[0], extend='both')
    cb.ax.set_yscale('log')

    pc = ax[1].pcolormesh(np.arange(100).reshape(10, 10)+1)
    cb = fig.colorbar(pc, ax=ax[1], extend='both')
    cb.ax.set_ylim(20, 90)

