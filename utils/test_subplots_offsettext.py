
def test_subplots_offsettext():
    x = np.arange(0, 1e10, 1e9)
    y = np.arange(0, 100, 10)+1e5
    fig, axs = plt.subplots(2, 2, sharex='col', sharey='all')
    axs[0, 0].plot(x, x)
    axs[1, 0].plot(x, x)
    axs[0, 1].plot(y, x)
    axs[1, 1].plot(y, x)

