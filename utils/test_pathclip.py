
def test_pathclip():
    np.random.seed(19680801)
    mpl.rcParams.update({'font.family': 'serif', 'pgf.rcfonts': False})
    fig, axs = plt.subplots(1, 2)

    axs[0].plot([0., 1e100], [0., 1e100])
    axs[0].set_xlim(0, 1)
    axs[0].set_ylim(0, 1)

    axs[1].scatter([0, 1], [1, 1])
    axs[1].hist(np.random.normal(size=1000), bins=20, range=[-10, 10])
    axs[1].set_xscale('log')

    fig.savefig(BytesIO(), format="pdf")  # No image comparison.

