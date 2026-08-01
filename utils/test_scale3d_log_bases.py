
def test_scale3d_log_bases():
    """Test log scale with different bases and subs."""
    fig, axs = plt.subplots(2, 2, subplot_kw={'projection': '3d'}, figsize=(10, 8))
    x, y, z = _make_log_data()

    for ax, base, title in [(axs[0, 0], 10, 'base=10'),
                            (axs[0, 1], 2, 'base=2'),
                            (axs[1, 0], np.e, 'base=e')]:
        ax.scatter(x, y, z, s=10)
        ax.set_xscale('log', base=base)
        ax.set_yscale('log', base=base)
        ax.set_zscale('log', base=base)
        ax.set_title(title)
        if base == np.e:
            # Format tick labels as e^n instead of 2.718...^n
            def fmt_e(x, pos=None):
                if x <= 0:
                    return ''
                exp = np.log(x)
                if np.isclose(exp, round(exp)):
                    return r'$e^{%d}$' % round(exp)
                return ''
            ax.xaxis.set_major_formatter(fmt_e)
            ax.yaxis.set_major_formatter(fmt_e)
            ax.zaxis.set_major_formatter(fmt_e)

    # subs
    axs[1, 1].scatter(x, y, z, s=10)
    axs[1, 1].set_xscale('log', subs=[2, 5])
    axs[1, 1].set_yscale('log', subs=[2, 5])
    axs[1, 1].set_zscale('log', subs=[2, 5])
    axs[1, 1].set_title('subs=[2,5]')

