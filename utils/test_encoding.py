
def test_encoding(mocker, log_mock):
    mi_cfg = cli.Config(**BASE_CONFIG.config_values)
    mi_cfg.config_values.update(MI_CONFIG.config_values)
    raw_cfg = cli.Config(**BASE_CONFIG.config_values)
    raw_cfg.config_values.update(RAW_CONFIG.config_values)
    mappings = {
        MIHarvester: mi_cfg,
        RawHarvester: raw_cfg,
        CCHarvester: CC_CONFIG,
    }
    if sys.version_info[0] < 3:
        target = 'data/__init__.py'
    else:
        target = 'data/py3unicode.py'
    fnames = [
        os.path.join(DIRNAME, target),
        # This one will fail if detect_encoding() removes the first lines
        # See #133
        os.path.join(DIRNAME, 'data/no_encoding.py'),
    ]
    for h_class, cfg in mappings.items():
        for f in fnames:
            harvester = h_class([f], cfg)
            assert not any(
                ['error' in kw for msg, args, kw in harvester.to_terminal()]
            )


def test_encoding(temp_hdfstore):
    df = DataFrame({"A": "foo", "B": "bar"}, index=range(5))
    df.loc[2, "A"] = np.nan
    df.loc[3, "B"] = np.nan
    temp_hdfstore.append("df", df, encoding="ascii")
    tm.assert_frame_equal(temp_hdfstore["df"], df)

    expected = df.reindex(columns=["A"])
    result = temp_hdfstore.select("df", Term("columns=A", encoding="ascii"))
    tm.assert_frame_equal(result, expected)

