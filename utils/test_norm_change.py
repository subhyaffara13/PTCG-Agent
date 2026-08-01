
def test_norm_change(fig_test, fig_ref):
    # LogNorm should not mask anything invalid permanently.
    data = np.full((5, 5), 1, dtype=np.float64)
    data[0:2, :] = -1

    masked_data = np.ma.array(data, mask=False)
    masked_data.mask[0:2, 0:2] = True

    cmap = mpl.colormaps['viridis'].with_extremes(under='w')

    ax = fig_test.subplots()
    im = ax.imshow(data, norm=colors.LogNorm(vmin=0.5, vmax=1),
                   extent=(0, 5, 0, 5), interpolation='nearest', cmap=cmap)
    im.set_norm(colors.Normalize(vmin=-2, vmax=2))
    im = ax.imshow(masked_data, norm=colors.LogNorm(vmin=0.5, vmax=1),
                   extent=(5, 10, 5, 10), interpolation='nearest', cmap=cmap)
    im.set_norm(colors.Normalize(vmin=-2, vmax=2))
    ax.set(xlim=(0, 10), ylim=(0, 10))

    ax = fig_ref.subplots()
    ax.imshow(data, norm=colors.Normalize(vmin=-2, vmax=2),
              extent=(0, 5, 0, 5), interpolation='nearest', cmap=cmap)
    ax.imshow(masked_data, norm=colors.Normalize(vmin=-2, vmax=2),
              extent=(5, 10, 5, 10), interpolation='nearest', cmap=cmap)
    ax.set(xlim=(0, 10), ylim=(0, 10))

