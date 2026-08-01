
def test_count_bitmaps():
    def count_tag(fig, tag):
        with BytesIO() as fd:
            fig.savefig(fd, format='svg')
            buf = fd.getvalue().decode()
        return buf.count(f"<{tag}")

    # No rasterized elements
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(1, 1, 1)
    ax1.set_axis_off()
    for n in range(5):
        ax1.plot([0, 20], [0, n], "b-", rasterized=False)
    assert count_tag(fig1, "image") == 0
    assert count_tag(fig1, "path") == 6  # axis patch plus lines

    # rasterized can be merged
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(1, 1, 1)
    ax2.set_axis_off()
    for n in range(5):
        ax2.plot([0, 20], [0, n], "b-", rasterized=True)
    assert count_tag(fig2, "image") == 1
    assert count_tag(fig2, "path") == 1  # axis patch

    # rasterized can't be merged without affecting draw order
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(1, 1, 1)
    ax3.set_axis_off()
    for n in range(5):
        ax3.plot([0, 20], [n, 0], "b-", rasterized=False)
        ax3.plot([0, 20], [0, n], "b-", rasterized=True)
    assert count_tag(fig3, "image") == 5
    assert count_tag(fig3, "path") == 6

    # rasterized whole axes
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(1, 1, 1)
    ax4.set_axis_off()
    ax4.set_rasterized(True)
    for n in range(5):
        ax4.plot([0, 20], [n, 0], "b-", rasterized=False)
        ax4.plot([0, 20], [0, n], "b-", rasterized=True)
    assert count_tag(fig4, "image") == 1
    assert count_tag(fig4, "path") == 1

    # rasterized can be merged, but inhibited by suppressComposite
    fig5 = plt.figure()
    fig5.suppressComposite = True
    ax5 = fig5.add_subplot(1, 1, 1)
    ax5.set_axis_off()
    for n in range(5):
        ax5.plot([0, 20], [0, n], "b-", rasterized=True)
    assert count_tag(fig5, "image") == 5
    assert count_tag(fig5, "path") == 1  # axis patch

