
def test_svg_default_metadata(monkeypatch):
    # Values have been predefined for 'Creator', 'Date', 'Format', and 'Type'.
    monkeypatch.setenv('SOURCE_DATE_EPOCH', '19680801')

    fig, ax = plt.subplots()
    with BytesIO() as fd:
        fig.savefig(fd, format='svg')
        buf = fd.getvalue().decode()

    # Creator
    assert mpl.__version__ in buf
    # Date
    assert '1970-08-16' in buf
    # Format
    assert 'image/svg+xml' in buf
    # Type
    assert 'StillImage' in buf

    # Now make sure all the default metadata can be cleared.
    with BytesIO() as fd:
        fig.savefig(fd, format='svg', metadata={'Date': None, 'Creator': None,
                                                'Format': None, 'Type': None})
        buf = fd.getvalue().decode()

    # Creator
    assert mpl.__version__ not in buf
    # Date
    assert '1970-08-16' not in buf
    # Format
    assert 'image/svg+xml' not in buf
    # Type
    assert 'StillImage' not in buf

