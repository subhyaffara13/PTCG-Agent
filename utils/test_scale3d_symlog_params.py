
def test_scale3d_symlog_params():
    """Test symlog scale with different linthresh values."""
    fig, axs = plt.subplots(1, 2, subplot_kw={'projection': '3d'})

    # Data spanning negative, zero, and positive
    t = np.linspace(-3, 3, 50)
    x = np.sinh(t) * 10
    y = t ** 3
    z = np.sign(t) * np.abs(t) ** 2

    for ax, linthresh in [(axs[0], 0.1), (axs[1], 10)]:
        ax.scatter(x, y, z, c=np.abs(z), cmap='viridis', s=10)
        ax.set_xscale('symlog', linthresh=linthresh)
        ax.set_yscale('symlog', linthresh=linthresh)
        ax.set_zscale('symlog', linthresh=linthresh)
        ax.set_title(f'linthresh={linthresh}')

