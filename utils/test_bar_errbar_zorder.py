
def test_bar_errbar_zorder():
    # Check that the zorder of errorbars is always greater than the bar they
    # are plotted on
    fig, ax = plt.subplots()
    x = [1, 2, 3]
    barcont = ax.bar(x=x, height=x, yerr=x, capsize=5, zorder=3)

    data_line, caplines, barlinecols = barcont.errorbar.lines
    for bar in barcont.patches:
        for capline in caplines:
            assert capline.zorder > bar.zorder
        for barlinecol in barlinecols:
            assert barlinecol.zorder > bar.zorder

