
def test_find_invalid(tmp_path):

    with pytest.raises(FileNotFoundError):
        get_font(tmp_path / 'non-existent-font-name.ttf')

    with pytest.raises(FileNotFoundError):
        get_font(str(tmp_path / 'non-existent-font-name.ttf'))

    with pytest.raises(FileNotFoundError):
        get_font(bytes(tmp_path / 'non-existent-font-name.ttf'))

