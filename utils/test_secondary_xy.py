
def test_secondary_xy():
    fig, axs = plt.subplots(1, 2, figsize=(10, 5), constrained_layout=True)

    def invert(x):
        with np.errstate(divide='ignore'):
            return 1 / x

    for nn, ax in enumerate(axs):
        ax.plot(np.arange(2, 11), np.arange(2, 11))
        if nn == 0:
            secax = ax.secondary_xaxis
        else:
            secax = ax.secondary_yaxis

        secax(0.2, functions=(invert, invert))
        secax(0.4, functions=(lambda x: 2 * x, lambda x: x / 2))
        secax(0.6, functions=(lambda x: x**2, lambda x: x**(1/2)))
        secax(0.8)
        secax("top" if nn == 0 else "right", functions=_Translation(2))
        secax(6.25, transform=ax.transData)

