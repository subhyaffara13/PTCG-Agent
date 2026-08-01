
def test_czt_vs_fft():
    rng = np.random.RandomState(123)  # Deterministic randomness
    random_lengths = rng.exponential(100000, size=10).astype('int')
    for n in random_lengths:
        a = rng.randn(n)
        xp_assert_close(czt(a), fft(a), rtol=1e-11)

