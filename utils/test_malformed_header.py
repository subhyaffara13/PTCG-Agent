
def test_malformed_header(afm_data, caplog):
    fh = BytesIO(afm_data)
    with caplog.at_level(logging.ERROR):
        _afm._parse_header(fh)

    assert len(caplog.records) == 1

