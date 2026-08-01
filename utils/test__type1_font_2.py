
def test_Type1Font_2():
    filename = os.path.join(os.path.dirname(__file__), 'data',
                            'Courier10PitchBT-Bold.pfb')
    font = t1f.Type1Font(filename)
    assert font.prop['Weight'] == 'Bold'
    assert font.prop['isFixedPitch']
    assert font.prop['Encoding'][65] == 'A'  # the font uses StandardEncoding
    (pos0, pos1), = font._pos['Encoding']
    assert font.parts[0][pos0:pos1] == b'/Encoding StandardEncoding'
    assert font._abbr['ND'] == '|-'

