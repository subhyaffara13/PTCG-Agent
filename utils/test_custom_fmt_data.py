
def test_custom_fmt_data():
    ax = plt.subplot(projection="polar")
    def millions(x):
        return '$%1.1fM' % (x*1e-6)

    # Test only x formatter
    ax.fmt_xdata = None
    ax.fmt_ydata = millions
    assert ax.format_coord(12, 2e7) == "θ=3.8197186342π (687.54935416°), r=$20.0M"
    assert ax.format_coord(1234, 2e6) == "θ=392.794399551π (70702.9919191°), r=$2.0M"
    assert ax.format_coord(3, 100) == "θ=0.95493π (171.887°), r=$0.0M"

    # Test only y formatter
    ax.fmt_xdata = millions
    ax.fmt_ydata = None
    assert ax.format_coord(2e5, 1) == "θ=$0.2M, r=1.000"
    assert ax.format_coord(1, .1) == "θ=$0.0M, r=0.100"
    assert ax.format_coord(1e6, 0.005) == "θ=$1.0M, r=0.005"

    # Test both x and y formatters
    ax.fmt_xdata = millions
    ax.fmt_ydata = millions
    assert ax.format_coord(2e6, 2e4*3e5) == "θ=$2.0M, r=$6000.0M"
    assert ax.format_coord(1e18, 12891328123) == "θ=$1000000000000.0M, r=$12891.3M"
    assert ax.format_coord(63**7, 1081968*1024) == "θ=$3938980.6M, r=$1107.9M"

