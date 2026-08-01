
def test_given_colors_levels_and_extends():
    # Remove this line when this test image is regenerated.
    plt.rcParams['pcolormesh.snap'] = False

    _, axs = plt.subplots(2, 4)

    data = np.arange(12).reshape(3, 4)

    colors = ['red', 'yellow', 'pink', 'blue', 'black']
    levels = [2, 4, 8, 10]

    for i, ax in enumerate(axs.flat):
        filled = i % 2 == 0.
        extend = ['neither', 'min', 'max', 'both'][i // 2]

        if filled:
            # If filled, we have 3 colors with no extension,
            # 4 colors with one extension, and 5 colors with both extensions
            first_color = 1 if extend in ['max', 'neither'] else None
            last_color = -1 if extend in ['min', 'neither'] else None
            c = ax.contourf(data, colors=colors[first_color:last_color],
                            levels=levels, extend=extend)
        else:
            # If not filled, we have 4 levels and 4 colors
            c = ax.contour(data, colors=colors[:-1],
                           levels=levels, extend=extend)

        plt.colorbar(c, ax=ax)

