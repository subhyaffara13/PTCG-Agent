
def check_step_determinism(env: gym.Env, seed=123):
    """Check that the environment steps deterministically after reset.

    Note: This check assumes that seeded `reset()` is deterministic (it must have passed `check_reset_seed`) and that `step()` returns valid values (passed `env_step_passive_checker`).
    Note: A single step should be enough to assert that the state transition function is deterministic (at least for most environments).

    Raises:
        AssertionError: The environment cannot be step deterministically after resetting with a random seed,
            or it truncates after 1 step.
    """
    if env.spec is not None and env.spec.nondeterministic is True:
        return

    env.action_space.seed(seed)
    action = env.action_space.sample()

    env.reset(seed=seed)
    obs_0, rew_0, term_0, trunc_0, info_0 = env.step(action)
    seeded_rng: np.random.Generator = deepcopy(env.unwrapped._np_random)

    env.reset(seed=seed)
    obs_1, rew_1, term_1, trunc_1, info_1 = env.step(action)

    assert (
        env.unwrapped._np_random.bit_generator.state  # pyright: ignore [reportOptionalMemberAccess]
        == seeded_rng.bit_generator.state
    ), "The `.np_random` is not properly been updated after step."

    assert data_equivalence(
        obs_0, obs_1
    ), "Deterministic step observations are not equivalent for the same seed and action"
    if not data_equivalence(obs_0, obs_1, exact=True):
        logger.warn(
            "Step observations are not equal although similar given the same seed and action"
        )

    assert data_equivalence(
        rew_0, rew_1
    ), "Deterministic step rewards are not equivalent for the same seed and action"
    if not data_equivalence(rew_0, rew_1, exact=True):
        logger.warn(
            "Step rewards are not equal although similar given the same seed and action"
        )

    assert data_equivalence(
        term_0, term_1, exact=True
    ), "Deterministic step termination are not equivalent for the same seed and action"
    assert (
        trunc_0 is False and trunc_1 is False
    ), "Environment truncates after 1 step, something has gone very wrong."

    assert data_equivalence(
        info_0,
        info_1,
    ), "Deterministic step info are not equivalent for the same seed and action"
    if not data_equivalence(info_0, info_1, exact=True):
        logger.warn(
            "Step info are not equal although similar given the same seed and action"
        )

