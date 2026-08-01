
def test_specgram_fs_none():
    """Test axes.specgram when Fs is None, should not throw error."""
    spec, freqs, t, im = plt.specgram(np.ones(300), Fs=None, scale='linear')
    xmin, xmax, freq0, freq1 = im.get_extent()
    assert xmin == 32 and xmax == 96

