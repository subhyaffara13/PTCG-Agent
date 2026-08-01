
def check_env(
    env: gym.Env,
    warn: bool = None,
    skip_render_check: bool = False,
    skip_close_check: bool = False,
):
    """Check that an environment follows Gymnasium's API.

    .. py:currentmodule:: gymnasium.Env

    To ensure that an environment is implemented "correctly", ``check_env`` checks that the :attr:`observation_space` and :attr:`action_space` are correct.
    Furthermore, the function will call the :meth:`reset`, :meth:`step` and :meth:`render` functions with a variety of values.

    We highly recommend users call this function after an environment is constructed and within a project's continuous integration to keep an environment update with Gymnasium's API.

    Args:
        env: The Gym environment that will be checked
        warn: Ignored, previously silenced particular warnings
        skip_render_check: Whether to skip the checks for the render method. False by default (useful for the CI)
        skip_close_check: Whether to skip the checks for the close method. False by default
    """
    if warn is not None:
        logger.warn("`check_env(warn=...)` parameter is now ignored.")

    if not isinstance(env, gym.Env):
        if (
            str(env.__class__.__base__) == "<class 'gym.core.Env'>"
            or str(env.__class__.__base__) == "<class 'gym.core.Wrapper'>"
        ):
            raise TypeError(
                "Gym is incompatible with Gymnasium, please update the environment class to `gymnasium.Env`. "
                "See https://gymnasium.farama.org/introduction/create_custom_env/ for more info."
            )
        else:
            raise TypeError(
                f"The environment must inherit from the gymnasium.Env class, actual class: {type(env)}. "
                "See https://gymnasium.farama.org/introduction/create_custom_env/ for more info."
            )
    if env.unwrapped is not env:
        logger.warn(
            f"The environment ({env}) is different from the unwrapped version ({env.unwrapped}). This could effect the environment checker as the environment most likely has a wrapper applied to it. We recommend using the raw environment for `check_env` using `env.unwrapped`."
        )

    if env.metadata.get("jax", False):
        env = gym.wrappers.JaxToNumpy(env)
    elif env.metadata.get("torch", False):
        env = gym.wrappers.TorchToNumpy(env)

    # ============= Check the spaces (observation and action) ================
    if not hasattr(env, "action_space"):
        raise AttributeError(
            "The environment must specify an action space. See https://gymnasium.farama.org/introduction/create_custom_env/ for more info."
        )
    check_action_space(env.action_space)
    check_space_limit(env.action_space, "action")

    if not hasattr(env, "observation_space"):
        raise AttributeError(
            "The environment must specify an observation space. See https://gymnasium.farama.org/introduction/create_custom_env/ for more info."
        )
    check_observation_space(env.observation_space)
    check_space_limit(env.observation_space, "observation")

    # ==== Check the reset method ====
    check_seed_deprecation(env)
    check_reset_return_info_deprecation(env)
    check_reset_return_type(env)
    check_reset_seed_determinism(env)
    check_reset_options(env)

    # ============ Check the returned values ===============
    env_reset_passive_checker(env)
    env_step_passive_checker(env, env.action_space.sample())

    # ==== Check the step method ====
    check_step_determinism(env)

    # ==== Check the render method and the declared render modes ====
    if not skip_render_check:
        if env.render_mode is not None:
            env_render_passive_checker(env)

        if env.spec is not None:
            for render_mode in env.metadata["render_modes"]:
                new_env = env.spec.make(render_mode=render_mode)
                new_env.reset()
                env_render_passive_checker(new_env)
                new_env.close()
        else:
            logger.warn(
                "Not able to test alternative render modes due to the environment not having a spec. Try instantiating the environment through `gymnasium.make`"
            )

    if not skip_close_check and env.spec is not None:
        new_env = env.spec.make()
        new_env.close()
        try:
            new_env.close()
        except Exception as e:
            logger.warn(
                f"Calling `env.close()` on the closed environment should be allowed, but it raised an exception: {e}"
            )


def check_env(env: gym.Env, warn: bool = None, skip_render_check: bool = False):
    """Check that an environment follows Gym API.

    This is an invasive function that calls the environment's reset and step.

    This is particularly useful when using a custom environment.
    Please take a look at https://www.gymlibrary.dev/content/environment_creation/
    for more information about the API.

    Args:
        env: The Gym environment that will be checked
        warn: Ignored
        skip_render_check: Whether to skip the checks for the render method. True by default (useful for the CI)
    """
    if warn is not None:
        logger.warn("`check_env(warn=...)` parameter is now ignored.")

    assert isinstance(
        env, gym.Env
    ), "The environment must inherit from the gym.Env class. See https://www.gymlibrary.dev/content/environment_creation/ for more info."

    if env.unwrapped is not env:
        logger.warn(
            f"The environment ({env}) is different from the unwrapped version ({env.unwrapped}). This could effect the environment checker as the environment most likely has a wrapper applied to it. We recommend using the raw environment for `check_env` using `env.unwrapped`."
        )

    # ============= Check the spaces (observation and action) ================
    assert hasattr(
        env, "action_space"
    ), "The environment must specify an action space. See https://www.gymlibrary.dev/content/environment_creation/ for more info."
    check_action_space(env.action_space)
    check_space_limit(env.action_space, "action")

    assert hasattr(
        env, "observation_space"
    ), "The environment must specify an observation space. See https://www.gymlibrary.dev/content/environment_creation/ for more info."
    check_observation_space(env.observation_space)
    check_space_limit(env.observation_space, "observation")

    # ==== Check the reset method ====
    check_seed_deprecation(env)
    check_reset_return_info_deprecation(env)
    check_reset_return_type(env)
    check_reset_seed(env)
    check_reset_options(env)

    # ============ Check the returned values ===============
    env_reset_passive_checker(env)
    env_step_passive_checker(env, env.action_space.sample())

    # ==== Check the render method and the declared render modes ====
    if not skip_render_check:
        if env.render_mode is not None:
            env_render_passive_checker(env)

