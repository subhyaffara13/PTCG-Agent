
def test_auto_column():
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)

    # iterable list input
    ax1.axis('off')
    tb1 = ax1.table(
        cellText=[['Fit Text', 2],
                  ['very long long text, Longer text than default', 1]],
        rowLabels=["A", "B"],
        colLabels=["Col1", "Col2"],
        loc="center")
    tb1.auto_set_font_size(False)
    tb1.set_fontsize(12)
    tb1.auto_set_column_width([-1, 0, 1])

    # iterable tuple input
    ax2.axis('off')
    tb2 = ax2.table(
        cellText=[['Fit Text', 2],
                  ['very long long text, Longer text than default', 1]],
        rowLabels=["A", "B"],
        colLabels=["Col1", "Col2"],
        loc="center")
    tb2.auto_set_font_size(False)
    tb2.set_fontsize(12)
    tb2.auto_set_column_width((-1, 0, 1))

    # 3 single inputs
    ax3.axis('off')
    tb3 = ax3.table(
        cellText=[['Fit Text', 2],
                  ['very long long text, Longer text than default', 1]],
        rowLabels=["A", "B"],
        colLabels=["Col1", "Col2"],
        loc="center")
    tb3.auto_set_font_size(False)
    tb3.set_fontsize(12)
    tb3.auto_set_column_width(-1)
    tb3.auto_set_column_width(0)
    tb3.auto_set_column_width(1)

    # 4 this used to test non-integer iterable input, which did nothing, but only
    # remains to avoid re-generating the test image.
    ax4.axis('off')
    tb4 = ax4.table(
        cellText=[['Fit Text', 2],
                  ['very long long text, Longer text than default', 1]],
        rowLabels=["A", "B"],
        colLabels=["Col1", "Col2"],
        loc="center")
    tb4.auto_set_font_size(False)
    tb4.set_fontsize(12)

