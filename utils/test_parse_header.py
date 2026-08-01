
def test_parse_header():
    fh = BytesIO(AFM_TEST_DATA)
    header = _afm._parse_header(fh)
    assert header == {
        'StartFontMetrics': 2.0,
        'FontName': 'MyFont-Bold',
        'EncodingScheme': 'FontSpecific',
        'FullName': 'My Font Bold',
        'FamilyName': 'Test Fonts',
        'Weight': 'Bold',
        'ItalicAngle': 0.0,
        'IsFixedPitch': False,
        'UnderlinePosition': -100,
        'UnderlineThickness': 56.789,
        'Version': '001.000',
        'Notice': b'Copyright \xa9 2017 No one.',
        'FontBBox': [0, -321, 1234, 369],
        'StartCharMetrics': 3,
    }

