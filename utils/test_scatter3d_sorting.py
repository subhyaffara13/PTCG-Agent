import itertools

def test_scatter3d_sorting(fig_ref, fig_test):
    """Test that marker properties are correctly sorted."""

    y, x = np.mgrid[:10, :10]
    z = np.arange(x.size).reshape(x.shape)
    depthshade = False

    sizes = np.full(z.shape, 25)
    sizes[0::2, 0::2] = 100
    sizes[1::2, 1::2] = 100

    facecolors = np.full(z.shape, 'C0')
    facecolors[:5, :5] = 'C1'
    facecolors[6:, :4] = 'C2'
    facecolors[6:, 6:] = 'C3'

    edgecolors = np.full(z.shape, 'C4')
    edgecolors[1:5, 1:5] = 'C5'
    edgecolors[5:9, 1:5] = 'C6'
    edgecolors[5:9, 5:9] = 'C7'

    linewidths = np.full(z.shape, 2)
    linewidths[0::2, 0::2] = 5
    linewidths[1::2, 1::2] = 5

    x, y, z, sizes, facecolors, edgecolors, linewidths = (
        a.flatten()
        for a in [x, y, z, sizes, facecolors, edgecolors, linewidths]
    )

    ax_ref = fig_ref.add_subplot(projection='3d')
    sets = (np.unique(a) for a in [sizes, facecolors, edgecolors, linewidths])
    for s, fc, ec, lw in itertools.product(*sets):
        subset = (
            (sizes != s) |
            (facecolors != fc) |
            (edgecolors != ec) |
            (linewidths != lw)
        )
        subset = np.ma.masked_array(z, subset, dtype=float)

        # When depth shading is disabled, the colors are passed through as
        # single-item lists; this triggers single path optimization. The
        # following reshaping is a hack to disable that, since the optimization
        # would not occur for the full scatter which has multiple colors.
        fc = np.repeat(fc, sum(~subset.mask))

        ax_ref.scatter(x, y, subset, s=s, fc=fc, ec=ec, lw=lw, alpha=1,
                       depthshade=depthshade)

    ax_test = fig_test.add_subplot(projection='3d')
    ax_test.scatter(x, y, z, s=sizes, fc=facecolors, ec=edgecolors,
                    lw=linewidths, alpha=1, depthshade=depthshade)

