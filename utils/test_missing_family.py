
def test_missing_family(caplog):
    plt.rcParams["font.sans-serif"] = ["this-font-does-not-exist"]
    with caplog.at_level("WARNING"):
        findfont("sans")
    assert [rec.getMessage() for rec in caplog.records] == [
        "findfont: Font family ['sans'] not found. "
        "Falling back to DejaVu Sans.",
        "findfont: Generic family 'sans' not found because none of the "
        "following families were found: this-font-does-not-exist",
    ]

