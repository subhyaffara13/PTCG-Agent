
def test_no_silent_downcasting_deprecated():
    # GH#59502
    with tm.assert_produces_warning(Pandas4Warning, match="is deprecated"):
        cf.get_option("future.no_silent_downcasting")
    with tm.assert_produces_warning(Pandas4Warning, match="is deprecated"):
        cf.set_option("future.no_silent_downcasting", True)

