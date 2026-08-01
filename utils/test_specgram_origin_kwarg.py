
def test_specgram_origin_kwarg():
    """Ensure passing origin as a kwarg raises a TypeError."""
    t = np.arange(500)
    signal = np.sin(t)

    with pytest.raises(TypeError):
        plt.specgram(signal, origin='lower')

