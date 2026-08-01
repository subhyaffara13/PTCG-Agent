
def test_spawn_negative_n_children():
    """Test that spawn raises ValueError for negative n_children."""
    from numpy.random.bit_generator import SeedlessSeedSequence

    rng = np.random.default_rng(42)
    seq = rng.bit_generator.seed_seq

    # Test SeedSequence.spawn
    with pytest.raises(ValueError, match="n_children must be non-negative"):
        seq.spawn(-1)

    # Test SeedlessSeedSequence.spawn
    seedless = SeedlessSeedSequence()
    with pytest.raises(ValueError, match="n_children must be non-negative"):
        seedless.spawn(-1)

    # Test BitGenerator.spawn
    with pytest.raises(ValueError, match="n_children must be non-negative"):
        rng.bit_generator.spawn(-1)

    # Test Generator.spawn
    with pytest.raises(ValueError, match="n_children must be non-negative"):
        rng.spawn(-1)

