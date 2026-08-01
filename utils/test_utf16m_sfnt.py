
def test_utf16m_sfnt():
    try:
        # seguisbi = Microsoft Segoe UI Semibold
        entry = next(entry for entry in fontManager.ttflist
                     if Path(entry.fname).name == "seguisbi.ttf")
    except StopIteration:
        pytest.skip("Couldn't find seguisbi.ttf font to test against.")
    else:
        # Check that we successfully read "semibold" from the font's sfnt table
        # and set its weight accordingly.
        assert entry.weight == 600

