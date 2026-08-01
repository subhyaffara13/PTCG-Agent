
def test_1D():
    # Test of 1D version of the transforms

    rng = np.random.RandomState(0)  # Deterministic randomness

    # Random signals
    lengths = rng.randint(8, 200, 20)
    np.append(lengths, 1)
    for length in lengths:
        x = rng.random(length)
        check_zoom_fft(x)
        check_czt(x)

    # Gauss
    t = np.linspace(-2, 2, 128)
    x = np.exp(-t**2/0.01)
    check_zoom_fft(x)

    # Linear
    x = [1, 2, 3, 4, 5, 6, 7]
    check_zoom_fft(x)

    # Check near powers of two
    check_zoom_fft(range(126-31))
    check_zoom_fft(range(127-31))
    check_zoom_fft(range(128-31))
    check_zoom_fft(range(129-31))
    check_zoom_fft(range(130-31))

    # Check transform on n-D array input
    x = np.reshape(np.arange(3*2*28), (3, 2, 28))
    y1 = zoom_fft(x, [0, 2-2./28])
    y2 = zoom_fft(x[2, 0, :], [0, 2-2./28])
    xp_assert_close(y1[2, 0], y2, rtol=1e-13, atol=1e-12)

    y1 = zoom_fft(x, [0, 2], endpoint=False)
    y2 = zoom_fft(x[2, 0, :], [0, 2], endpoint=False)
    xp_assert_close(y1[2, 0], y2, rtol=1e-13, atol=1e-12)

    # Random (not a test condition)
    x = rng.rand(101)
    check_zoom_fft(x)

    # Spikes
    t = np.linspace(0, 1, 128)
    x = np.sin(2*np.pi*t*5)+np.sin(2*np.pi*t*13)
    check_zoom_fft(x)

    # Sines
    x = np.zeros(100, dtype=complex)
    x[[1, 5, 21]] = 1
    check_zoom_fft(x)

    # Sines plus complex component
    x += 1j*np.linspace(0, 0.5, x.shape[0])
    check_zoom_fft(x)

