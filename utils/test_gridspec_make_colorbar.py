
def test_gridspec_make_colorbar():
    plt.figure()
    data = np.arange(1200).reshape(30, 40)
    levels = [0, 200, 400, 600, 800, 1000, 1200]

    plt.subplot(121)
    plt.contourf(data, levels=levels)
    plt.colorbar(use_gridspec=True, orientation='vertical')

    plt.subplot(122)
    plt.contourf(data, levels=levels)
    plt.colorbar(use_gridspec=True, orientation='horizontal')

    plt.subplots_adjust(top=0.95, right=0.95, bottom=0.2, hspace=0.25)

