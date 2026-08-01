
def test_partial_usetex(caplog):
    caplog.set_level("WARNING")
    plt.figtext(.1, .1, "foo", usetex=True)
    plt.figtext(.2, .2, "bar", usetex=True)
    plt.savefig(io.BytesIO(), format="ps")
    record, = caplog.records  # asserts there's a single record.
    assert "as if usetex=False" in record.getMessage()

