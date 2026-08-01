
def test_fontentry_dataclass_invalid_path():
    with pytest.raises(FileNotFoundError):
        fontent = FontEntry(fname='/random', name='font-name')
        fontent._repr_html_()

