
def test_identification(capsys):
    """Test that .sav file with IDENTIFICATION section read correctly."""
    # gh-24278
    s = readsav(path.join(DATA_PATH, 'identification.sav'), verbose=True)
    # Check array read correctly
    pattern = np.array([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 2.0, 1.0])
    expected = np.sqrt(pattern[:, np.newaxis] ** 2 + pattern[np.newaxis, :] ** 2)
    expected = expected.astype('float32')
    assert_allclose(expected, s.a)
    # Check that the correct identification fields were printed out by verbose mode
    captured = capsys.readouterr()
    assert "Author: x86_64" in captured.out
    assert "Title: linux" in captured.out
    assert "ID Code: 8.4" in captured.out

