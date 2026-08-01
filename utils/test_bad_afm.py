
def test_bad_afm(afm_data):
    fh = BytesIO(afm_data)
    with pytest.raises(RuntimeError):
        _afm._parse_header(fh)

