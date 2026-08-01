
def test_log_scales():
    fig, ax = plt.subplots()
    ax.plot(np.log(np.linspace(0.1, 100)))
    ax.set_yscale('log', base=5.5)
    ax.invert_yaxis()
    ax.set_xscale('log', base=9.0)
    xticks, yticks = (
        [(t.get_loc(), t.label1.get_text()) for t in axis._update_ticks()]
        for axis in [ax.xaxis, ax.yaxis]
    )
    assert xticks == [
        (1.0, '$\\mathdefault{9^{0}}$'),
        (9.0, '$\\mathdefault{9^{1}}$'),
        (81.0, '$\\mathdefault{9^{2}}$'),
        (2.0, ''),
        (3.0, ''),
        (4.0, ''),
        (5.0, ''),
        (6.0, ''),
        (7.0, ''),
        (8.0, ''),
        (18.0, ''),
        (27.0, ''),
        (36.0, ''),
        (45.0, ''),
        (54.0, ''),
        (63.0, ''),
        (72.0, ''),
    ]
    assert yticks == [
        (0.18181818181818182, '$\\mathdefault{5.5^{-1}}$'),
        (1.0, '$\\mathdefault{5.5^{0}}$'),
        (5.5, '$\\mathdefault{5.5^{1}}$'),
        (0.36363636363636365, ''),
        (0.5454545454545454, ''),
        (0.7272727272727273, ''),
        (0.9090909090909092, ''),
        (2.0, ''),
        (3.0, ''),
        (4.0, ''),
        (5.0, ''),
    ]


def test_log_scales(fig_test, fig_ref):
    ax_test = fig_test.add_subplot(122, yscale='log', xscale='symlog')
    ax_test.axvline(24.1)
    ax_test.axhline(24.1)
    xlim = ax_test.get_xlim()
    ylim = ax_test.get_ylim()
    ax_ref = fig_ref.add_subplot(122, yscale='log', xscale='symlog')
    ax_ref.set(xlim=xlim, ylim=ylim)
    ax_ref.plot([24.1, 24.1], ylim, 'b')
    ax_ref.plot(xlim, [24.1, 24.1], 'b')

