
def test_patheffect2():

    ax2 = plt.subplot()
    arr = np.arange(25).reshape((5, 5))
    ax2.imshow(arr, interpolation='nearest')
    cntr = ax2.contour(arr, colors="k")
    cntr.set(path_effects=[path_effects.withStroke(linewidth=3, foreground="w")])

    clbls = ax2.clabel(cntr, fmt="%2.0f", use_clabeltext=True)
    plt.setp(clbls,
             path_effects=[path_effects.withStroke(linewidth=3,
                                                   foreground="w")])

