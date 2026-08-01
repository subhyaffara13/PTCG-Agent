
def test_large_prime_lengths():
    rng = np.random.RandomState(0)  # Deterministic randomness
    for N in (101, 1009, 10007):
        x = rng.rand(N)
        y = fft(x)
        y1 = czt(x)
        xp_assert_close(y, y1, rtol=1e-12)

