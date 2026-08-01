
def test_unknown_font(caplog):
    with caplog.at_level("WARNING"):
        mpl.rcParams["font.family"] = "this-font-does-not-exist"
        plt.figtext(.5, .5, "hello, world")
        plt.savefig(BytesIO(), format="pgf")
    assert "Ignoring unknown font: this-font-does-not-exist" in [
        r.getMessage() for r in caplog.records]

