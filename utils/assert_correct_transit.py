
def assert_correct_transit(
    obs_gym,
    reward_gym,
    done_gym,
    obs_jax,
    reward_jax,
    done_jax,
    atol: float = 1e-4,
):
    """Check that obs, reward, done transition outputs are correct."""
    if not done_gym:
        assert np.allclose(obs_gym, obs_jax, atol=atol)
    assert np.allclose(reward_gym, reward_jax, atol=atol)
    assert np.all(done_gym == done_jax)

