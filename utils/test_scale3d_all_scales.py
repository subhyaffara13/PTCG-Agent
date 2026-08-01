
def test_scale3d_all_scales():
    """Test all scale types with mixed scales on each axis."""
    fig, axs = plt.subplots(1, 2, subplot_kw={'projection': '3d'}, figsize=(10, 6))

    # Data that works across all scale types
    t = np.linspace(0.1, 0.9, 30)
    # x: positive for log/asinh, y: spans neg/pos for symlog, z: (0,1) for logit
    x = t * 100  # 10 to 90
    y = (t - 0.5) * 20  # -10 to 10
    z = t  # 0.1 to 0.9

    # Subplot 1: x=log, y=symlog, z=logit
    axs[0].scatter(x, y, z)
    axs[0].set(xscale='log', yscale='symlog', zscale='logit',
               xlabel='log', ylabel='symlog', zlabel='logit')

    # Subplot 2: x=asinh, y=linear, z=function (square root)
    axs[1].scatter(x, y, z)
    axs[1].set_xscale('asinh')
    axs[1].set_zscale('function', functions=(lambda v: v**0.5, lambda v: v**2))
    axs[1].set(xlabel='asinh', ylabel='linear', zlabel='function')

