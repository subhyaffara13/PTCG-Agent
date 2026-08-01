
def check_reset_seed_determinism(env: gym.Env):
    """Check that the environment can be reset with a seed.

    Args:
        env: The environment to check

    Raises:
        AssertionError: The environment cannot be reset with a random seed,
            even though `seed` or `kwargs` appear in the signature.
    """
    signature = inspect.signature(env.reset)
    if "seed" in signature.parameters or (
        "kwargs" in signature.parameters
        and signature.parameters["kwargs"].kind is inspect.Parameter.VAR_KEYWORD
    ):
        try:
            obs_1, info = env.reset(seed=123)
            assert (
                obs_1 in env.observation_space
            ), "The observation returned by `env.reset(seed=123)` is not within the observation space."
            assert (
                env.unwrapped._np_random is not None
            ), "Expects the random number generator to have been generated given a seed was passed to reset. Most likely the environment reset function does not call `super().reset(seed=seed)`."
            seed_123_rng_1 = deepcopy(env.unwrapped._np_random)

            obs_2, info = env.reset()
            assert (
                obs_2 in env.observation_space
            ), "The observation returned by `env.reset()` is not within the observation space."

            obs_3, info = env.reset(seed=123)
            assert (
                obs_3 in env.observation_space
            ), "The observation returned by `env.reset(seed=123)` is not within the observation space."
            seed_123_rng_3 = deepcopy(env.unwrapped._np_random)

            obs_4, info = env.reset()
            assert (
                obs_4 in env.observation_space
            ), "The observation returned by `env.reset()` is not within the observation space."

            if env.spec is not None and env.spec.nondeterministic is False:
                assert data_equivalence(
                    obs_1, obs_3
                ), "Using `env.reset(seed=123)` is non-deterministic as the observations are not equivalent."
                assert data_equivalence(
                    obs_2, obs_4
                ), "Using `env.reset(seed=123)` then `env.reset()` is non-deterministic as the observations are not equivalent."
                if not data_equivalence(obs_1, obs_3, exact=True):
                    logger.warn(
                        "Using `env.reset(seed=123)` observations are not equal although similar."
                    )
                if not data_equivalence(obs_2, obs_4, exact=True):
                    logger.warn(
                        "Using `env.reset(seed=123)` then `env.reset()` observations are not equal although similar."
                    )

            assert (
                seed_123_rng_1.bit_generator.state == seed_123_rng_3.bit_generator.state
            ), "Most likely the environment reset function does not call `super().reset(seed=seed)` as the random generates are not same when the same seeds are passed to `env.reset`."

            obs_5, info = env.reset(seed=456)
            assert (
                obs_5 in env.observation_space
            ), "The observation returned by `env.reset(seed=456)` is not within the observation space."
            assert (
                env.unwrapped._np_random.bit_generator.state
                != seed_123_rng_1.bit_generator.state
            ), "Most likely the environment reset function does not call `super().reset(seed=seed)` as the random number generators are not different when different seeds are passed to `env.reset`."

        except TypeError as e:
            raise AssertionError(
                "The environment cannot be reset with a random seed, even though `seed` or `kwargs` appear in the signature. "
                f"This should never happen, please report this issue. The error was: {e}"
            ) from e

        seed_param = signature.parameters.get("seed")
        # Check the default value is None
        if seed_param is not None and seed_param.default is not None:
            logger.warn(
                "The default seed argument in reset should be `None`, otherwise the environment will by default always be deterministic. "
                f"Actual default: {seed_param.default}"
            )
    else:
        raise gym.error.Error(
            "The `reset` method does not provide a `seed` or `**kwargs` keyword argument."
        )

