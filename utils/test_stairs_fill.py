
def test_stairs_fill(fig_test, fig_ref):
    h, bins = [1, 2, 3, 4, 2], [0, 1, 2, 3, 4, 5]
    bs = -2
    # Test
    test_axes = fig_test.subplots(2, 2).flatten()
    test_axes[0].stairs(h, bins, fill=True)
    test_axes[1].stairs(h, bins, orientation='horizontal', fill=True)
    test_axes[2].stairs(h, bins, baseline=bs, fill=True)
    test_axes[3].stairs(h, bins, baseline=bs, orientation='horizontal',
                        fill=True)

    # # Ref
    ref_axes = fig_ref.subplots(2, 2).flatten()
    ref_axes[0].fill_between(bins, np.append(h, h[-1]), step='post', lw=0)
    ref_axes[0].set_ylim(0, None)
    ref_axes[1].fill_betweenx(bins, np.append(h, h[-1]), step='post', lw=0)
    ref_axes[1].set_xlim(0, None)
    ref_axes[2].fill_between(bins, np.append(h, h[-1]),
                             np.ones(len(h)+1)*bs, step='post', lw=0)
    ref_axes[2].set_ylim(bs, None)
    ref_axes[3].fill_betweenx(bins, np.append(h, h[-1]),
                              np.ones(len(h)+1)*bs, step='post', lw=0)
    ref_axes[3].set_xlim(bs, None)

