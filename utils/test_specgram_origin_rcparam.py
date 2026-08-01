
def test_specgram_origin_rcparam(fig_test, fig_ref):
    """Test specgram ignores image.origin rcParam and uses origin 'upper'."""
    t = np.arange(500)
    signal = np.sin(t)

    plt.rcParams["image.origin"] = 'upper'

    # Reference: First graph using default origin in imshow (upper),
    fig_ref.subplots().specgram(signal)

    # Try to overwrite the setting trying to flip the specgram
    plt.rcParams["image.origin"] = 'lower'

    # Test: origin='lower' should be ignored
    fig_test.subplots().specgram(signal)

