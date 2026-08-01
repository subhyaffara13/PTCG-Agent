
def test_json_serialization(tmp_path):
    # Can't open a NamedTemporaryFile twice on Windows, so use a temporary
    # directory instead.
    json_dump(fontManager, tmp_path / "fontlist.json")
    copy = json_load(tmp_path / "fontlist.json")
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'findfont: Font family.*not found')
        for prop in ({'family': 'STIXGeneral'},
                     {'family': 'Bitstream Vera Sans', 'weight': 700},
                     {'family': 'no such font family'}):
            fp = FontProperties(**prop)
            assert (fontManager.findfont(fp, rebuild_if_missing=False) ==
                    copy.findfont(fp, rebuild_if_missing=False))

