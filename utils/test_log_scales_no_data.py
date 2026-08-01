
def test_log_scales_no_data():
    _, ax = plt.subplots()
    ax.set(xscale="log", yscale="log")
    ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
    assert ax.get_xlim() == ax.get_ylim() == (1, 10)

