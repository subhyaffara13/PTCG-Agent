
def test_huge_range_log(fig_test, fig_ref, x):
    # parametrize over bad lognorm -1 values and large range 1 -> 1e20
    data = np.full((5, 5), x, dtype=np.float64)
    data[0:2, :] = 1E20

    ax = fig_test.subplots()
    ax.imshow(data, norm=colors.LogNorm(vmin=1, vmax=data.max()),
              interpolation='nearest', cmap='viridis')

    data = np.full((5, 5), x, dtype=np.float64)
    data[0:2, :] = 1000

    ax = fig_ref.subplots()
    cmap = mpl.colormaps['viridis'].with_extremes(under='w')
    ax.imshow(data, norm=colors.Normalize(vmin=1, vmax=data.max()),
              interpolation='nearest', cmap=cmap)

