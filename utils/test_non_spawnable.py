
def test_non_spawnable():
    from numpy.random.bit_generator import ISeedSequence

    class FakeSeedSequence:
        def generate_state(self, n_words, dtype=np.uint32):
            return np.zeros(n_words, dtype=dtype)

    ISeedSequence.register(FakeSeedSequence)

    rng = np.random.default_rng(FakeSeedSequence())

    with pytest.raises(TypeError, match="The underlying SeedSequence"):
        rng.spawn(5)

    with pytest.raises(TypeError, match="The underlying SeedSequence"):
        rng.bit_generator.spawn(5)

