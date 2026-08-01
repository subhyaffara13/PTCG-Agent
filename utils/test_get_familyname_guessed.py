
def test_get_familyname_guessed():
    fh = BytesIO(AFM_TEST_DATA)
    font = _afm.AFM(fh)
    del font._header['FamilyName']  # remove FamilyName, so we have to guess
    assert font.get_familyname() == 'My Font'

