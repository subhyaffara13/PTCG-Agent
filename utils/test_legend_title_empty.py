
def test_legend_title_empty():
    # test that if we don't set the legend title, that
    # it comes back as an empty string, and that it is not
    # visible:
    fig, ax = plt.subplots()
    ax.plot(range(10), label="mock data")
    leg = ax.legend()
    assert leg.get_title().get_text() == ""
    assert not leg.get_title().get_visible()

