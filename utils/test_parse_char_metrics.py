
def test_parse_char_metrics():
    fh = BytesIO(AFM_TEST_DATA)
    _afm._parse_header(fh)  # position
    metrics = _afm._parse_char_metrics(fh)
    assert metrics == (
        {
            0: _afm.CharMetrics(250.0, 'space', (0, 0, 0, 0)),
            42: _afm.CharMetrics(1141.0, 'foo', (40, 60, 800, 360)),
            99: _afm.CharMetrics(583.0, 'bar', (40, -10, 543, 210)),
        },
        {
            'space': _afm.CharMetrics(250.0, 'space', (0, 0, 0, 0)),
            'foo': _afm.CharMetrics(1141.0, 'foo', (40, 60, 800, 360)),
            'bar': _afm.CharMetrics(583.0, 'bar', (40, -10, 543, 210)),
        }
    )

