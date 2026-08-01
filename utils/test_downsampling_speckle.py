
def test_downsampling_speckle():
    fig, axs = plt.subplots(1, 2, figsize=(5, 2.7), sharex=True, sharey=True,
                            layout="compressed")
    axs = axs.flatten()
    img = ((np.arange(1024).reshape(-1, 1) * np.ones(720)) // 50).T

    cm = plt.get_cmap("viridis").with_extremes(over="m")
    norm = colors.LogNorm(vmin=3, vmax=11)

    # old default cannot be tested because it creates over/under speckles
    # in the following that are machine dependent.

    axs[0].set_title("interpolation='auto', stage='rgba'")
    axs[0].imshow(np.triu(img), cmap=cm, norm=norm, interpolation_stage='rgba')

    # Should be same as previous
    axs[1].set_title("interpolation='auto', stage='auto'")
    axs[1].imshow(np.triu(img), cmap=cm, norm=norm)

