
def test_violinplot_color_specification(fig_test, fig_ref):
    # Ensures that setting colors in violinplot constructor works
    # the same way as setting the color of each object manually
    np.random.seed(19680801)
    data = [sorted(np.random.normal(0, std, 100)) for std in range(1, 4)]
    kwargs = {'showmeans': True,
              'showextrema': True,
              'showmedians': True
              }

    def color_violins(parts, facecolor=None, linecolor=None):
        """Helper to color parts manually."""
        if facecolor is not None:
            for pc in parts['bodies']:
                pc.set_facecolor(facecolor)
                # disable alpha Artist property to counter the legacy behavior
                # that applies an alpha of 0.3 to the bodies if no facecolor
                # was set
                pc.set_alpha(None)
        if linecolor is not None:
            for partname in ('cbars', 'cmins', 'cmaxes', 'cmeans', 'cmedians'):
                if partname in parts:
                    lc = parts[partname]
                    lc.set_edgecolor(linecolor)

    # Reference image
    ax = fig_ref.subplots(1, 3)
    parts0 = ax[0].violinplot(data, **kwargs)
    parts1 = ax[1].violinplot(data, **kwargs)
    parts2 = ax[2].violinplot(data, **kwargs)

    color_violins(parts0, facecolor=('r', 0.5), linecolor=('r', 0.2))
    color_violins(parts1, facecolor='r')
    color_violins(parts2, linecolor='r')

    # Test image
    ax = fig_test.subplots(1, 3)
    ax[0].violinplot(data, facecolor=('r', 0.5), linecolor=('r', 0.2), **kwargs)
    ax[1].violinplot(data, facecolor='r', **kwargs)
    ax[2].violinplot(data, linecolor='r', **kwargs)

