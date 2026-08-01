
def make(env_id: str, **env_kwargs):
    """A JAX-version of OpenAI's infamous env.make(env_name).


    Args:
      env_id: A string identifier for the environment.
      **env_kwargs: Keyword arguments to pass to the environment.


    Returns:
      A tuple of the environment and the default parameters.
    """
    if env_id not in registered_envs:
        raise ValueError(f"{env_id} is not in registered gymnax environments.")

    # 1. Classic OpenAI Control Tasks
    if env_id == "Pendulum-v1":
        env = pendulum.Pendulum(**env_kwargs)
    elif env_id == "CartPole-v1":
        env = cartpole.CartPole(**env_kwargs)
    elif env_id == "MountainCar-v0":
        env = mountain_car.MountainCar(**env_kwargs)
    elif env_id == "MountainCarContinuous-v0":
        env = continuous_mountain_car.ContinuousMountainCar(**env_kwargs)
    elif env_id == "Acrobot-v1":
        env = acrobot.Acrobot(**env_kwargs)

    # 2. DeepMind's bsuite environments
    elif env_id == "Catch-bsuite":
        env = catch.Catch(**env_kwargs)
    elif env_id == "DeepSea-bsuite":
        env = deep_sea.DeepSea(**env_kwargs)
    elif env_id == "DiscountingChain-bsuite":
        env = discounting_chain.DiscountingChain(**env_kwargs)
    elif env_id == "MemoryChain-bsuite":
        env = memory_chain.MemoryChain(**env_kwargs)
    elif env_id == "UmbrellaChain-bsuite":
        env = umbrella_chain.UmbrellaChain(**env_kwargs)
    elif env_id == "MNISTBandit-bsuite":
        env = mnist.MNISTBandit(**env_kwargs)
    elif env_id == "SimpleBandit-bsuite":
        env = bandit.SimpleBandit(**env_kwargs)

    # 3. MinAtar Environments
    elif env_id == "Asterix-MinAtar":
        env = asterix.MinAsterix(**env_kwargs)
    elif env_id == "Breakout-MinAtar":
        env = breakout.MinBreakout(**env_kwargs)
    elif env_id == "Freeway-MinAtar":
        env = freeway.MinFreeway(**env_kwargs)
    elif env_id == "Seaquest-MinAtar":
        raise NotImplementedError("Seaquest is not yet supported.")
        # env = MinSeaquest(**env_kwargs)
    elif env_id == "SpaceInvaders-MinAtar":
        env = space_invaders.MinSpaceInvaders(**env_kwargs)

    # 4. Miscellanoues Environments
    elif env_id == "BernoulliBandit-misc":
        env = bernoulli_bandit.BernoulliBandit(**env_kwargs)
    elif env_id == "GaussianBandit-misc":
        env = gaussian_bandit.GaussianBandit(**env_kwargs)
    elif env_id == "FourRooms-misc":
        env = rooms.FourRooms(**env_kwargs)
    elif env_id == "MetaMaze-misc":
        env = meta_maze.MetaMaze(**env_kwargs)
    elif env_id == "PointRobot-misc":
        env = point_robot.PointRobot(**env_kwargs)
    elif env_id == "Reacher-misc":
        env = reacher.Reacher(**env_kwargs)
    elif env_id == "Swimmer-misc":
        env = swimmer.Swimmer(**env_kwargs)
    elif env_id == "Pong-misc":
        env = pong.Pong(**env_kwargs)
    else:
        raise ValueError("Environment ID is not registered.")

    # Create a jax PRNG key for random seed control
    return env, env.default_params


def make(
    environment: str | "Environment" | Callable,
    configuration: dict[str, Any] | None = None,
    info: dict[str, Any] | None = None,
    steps: list[list[dict[str, Any]]] | None = None,
    logs: list[list[dict[str, Any]]] | None = None,
    debug: bool = False,
    state: list[dict[str, Any]] | None = None,
) -> "Environment":
    """
    Creates an instance of an Environment.

    Args:
        environment (str|Environment):
        configuration (dict, optional):
        info (dict, optional):
        steps (list, optional):
        debug (bool=False, optional): Render print() statments to stdout
        state (optional):

    Returns:
        Environment: Instance of a specific environment.
    """
    if configuration is None:
        configuration = {}
    if info is None:
        info = {}
    if steps is None:
        steps = []
    if logs is None:
        logs = []

    if has(environment, str) and has(environments, dict, path=[environment]):
        return Environment(
            **environments[environment],
            configuration=configuration,
            info=info,
            steps=steps,
            logs=logs,
            debug=debug,
            state=state,
        )
    elif callable(environment):
        return Environment(
            interpreter=environment,
            configuration=configuration,
            info=info,
            steps=steps,
            logs=logs,
            debug=debug,
            state=state,
        )
    elif has(environment, path=["interpreter"], is_callable=True):
        return Environment(
            **environment, configuration=configuration, info=info, steps=steps, logs=logs, debug=debug, state=state
        )
    raise InvalidArgument("Unknown Environment Specification")


def make() -> PresetType:
    return {
        "options": {
            "maxNesting": 20,  # Internal protection, recursion limit
            "html": True,  # Enable HTML tags in source,
            # this is just a shorthand for .enable(["html_inline", "html_block"])
            # used by the linkify rule:
            "linkify": False,  # autoconvert URL-like texts to links
            # used by the replacements and smartquotes rules
            # Enable some language-neutral replacements + quotes beautification
            "typographer": False,
            # used by the smartquotes rule:
            # Double + single quotes replacement pairs, when typographer enabled,
            # and smartquotes on. Could be either a String or an Array.
            #
            # For example, you can use '«»„“' for Russian, '„“‚‘' for German,
            # and ['«\xA0', '\xA0»', '‹\xA0', '\xA0›'] for French (including nbsp).
            "quotes": "\u201c\u201d\u2018\u2019",  # /* “”‘’ */
            # Renderer specific; these options are used directly in the HTML renderer
            "xhtmlOut": True,  # Use '/' to close single tags (<br />)
            "breaks": False,  # Convert '\n' in paragraphs into <br>
            "langPrefix": "language-",  # CSS language prefix for fenced blocks
            # Highlighter function. Should return escaped HTML,
            # or '' if the source string is not changed and should be escaped externally.
            # If result starts with <pre... internal wrapper is skipped.
            #
            # function (/*str, lang, attrs*/) { return ''; }
            #
            "highlight": None,
        },
        "components": {
            "core": {"rules": ["normalize", "block", "inline", "text_join"]},
            "block": {
                "rules": [
                    "blockquote",
                    "code",
                    "fence",
                    "heading",
                    "hr",
                    "html_block",
                    "lheading",
                    "list",
                    "reference",
                    "paragraph",
                ]
            },
            "inline": {
                "rules": [
                    "autolink",
                    "backticks",
                    "emphasis",
                    "entity",
                    "escape",
                    "html_inline",
                    "image",
                    "link",
                    "newline",
                    "text",
                ],
                "rules2": ["balance_pairs", "emphasis", "fragments_join"],
            },
        },
    }


def make() -> PresetType:
    return {
        "options": {
            "maxNesting": 100,  # Internal protection, recursion limit
            "html": False,  # Enable HTML tags in source
            # this is just a shorthand for .disable(["html_inline", "html_block"])
            # used by the linkify rule:
            "linkify": False,  # autoconvert URL-like texts to links
            # used by the replacements and smartquotes rules:
            # Enable some language-neutral replacements + quotes beautification
            "typographer": False,
            # used by the smartquotes rule:
            # Double + single quotes replacement pairs, when typographer enabled,
            # and smartquotes on. Could be either a String or an Array.
            # For example, you can use '«»„“' for Russian, '„“‚‘' for German,
            # and ['«\xA0', '\xA0»', '‹\xA0', '\xA0›'] for French (including nbsp).
            "quotes": "\u201c\u201d\u2018\u2019",  # /* “”‘’ */
            # Renderer specific; these options are used directly in the HTML renderer
            "xhtmlOut": False,  # Use '/' to close single tags (<br />)
            "breaks": False,  # Convert '\n' in paragraphs into <br>
            "langPrefix": "language-",  # CSS language prefix for fenced blocks
            # Highlighter function. Should return escaped HTML,
            # or '' if the source string is not changed and should be escaped externally.
            # If result starts with <pre... internal wrapper is skipped.
            #
            # function (/*str, lang, attrs*/) { return ''; }
            #
            "highlight": None,
        },
        "components": {"core": {}, "block": {}, "inline": {}},
    }


def make() -> PresetType:
    return {
        "options": {
            "maxNesting": 20,  # Internal protection, recursion limit
            "html": False,  # Enable HTML tags in source
            # this is just a shorthand for .disable(["html_inline", "html_block"])
            # used by the linkify rule:
            "linkify": False,  # autoconvert URL-like texts to links
            # used by the replacements and smartquotes rules:
            # Enable some language-neutral replacements + quotes beautification
            "typographer": False,
            # used by the smartquotes rule:
            # Double + single quotes replacement pairs, when typographer enabled,
            # and smartquotes on. Could be either a String or an Array.
            # For example, you can use '«»„“' for Russian, '„“‚‘' for German,
            # and ['«\xA0', '\xA0»', '‹\xA0', '\xA0›'] for French (including nbsp).
            "quotes": "\u201c\u201d\u2018\u2019",  # /* “”‘’ */
            # Renderer specific; these options are used directly in the HTML renderer
            "xhtmlOut": False,  # Use '/' to close single tags (<br />)
            "breaks": False,  # Convert '\n' in paragraphs into <br>
            "langPrefix": "language-",  # CSS language prefix for fenced blocks
            # Highlighter function. Should return escaped HTML,
            # or '' if the source string is not changed and should be escaped externally.
            # If result starts with <pre... internal wrapper is skipped.
            # function (/*str, lang, attrs*/) { return ''; }
            "highlight": None,
        },
        "components": {
            "core": {"rules": ["normalize", "block", "inline", "text_join"]},
            "block": {"rules": ["paragraph"]},
            "inline": {
                "rules": ["text"],
                "rules2": ["balance_pairs", "fragments_join"],
            },
        },
    }


def make(
    id: str | EnvSpec,
    max_episode_steps: int | None = None,
    disable_env_checker: bool | None = None,
    **kwargs: Any,
) -> Env:
    """Creates an environment previously registered with :meth:`gymnasium.register` or a :class:`EnvSpec`.

    To find all available environments use ``gymnasium.envs.registry.keys()`` for all valid ids.

    Args:
        id: A string for the environment id or a :class:`EnvSpec`. Optionally if using a string, a module to import can be included, e.g. ``'module:Env-v0'``.
            This is equivalent to importing the module first to register the environment followed by making the environment.
        max_episode_steps: Maximum length of an episode, can override the registered :class:`EnvSpec` ``max_episode_steps``
            with the value being passed to :class:`gymnasium.wrappers.TimeLimit`.
            Using ``max_episode_steps=-1`` will not apply the wrapper to the environment.
        disable_env_checker: If to add :class:`gymnasium.wrappers.PassiveEnvChecker`, ``None`` will default to the
            :class:`EnvSpec` ``disable_env_checker`` value otherwise use this value will be used.
        kwargs: Additional arguments to pass to the environment constructor.

    Returns:
        An instance of the environment with wrappers applied.

    Raises:
        Error: If the ``id`` doesn't exist in the :attr:`registry`

    Changelogs:
        v1.0.0 - `autoreset` and `apply_api_compatibility` was removed
    """
    if isinstance(id, EnvSpec):
        env_spec = id
        if not hasattr(env_spec, "additional_wrappers"):
            logger.warn(
                f"The env spec passed to `make` does not have a `additional_wrappers`, set it to an empty tuple. Env_spec={env_spec}"
            )
            env_spec.additional_wrappers = ()
    else:
        # For string id's, load the environment spec from the registry then make the environment spec
        assert isinstance(id, str)

        # The environment name can include an unloaded module in "module:env_name" style
        env_spec = _find_spec(id)

    assert isinstance(env_spec, EnvSpec)

    # Update the env spec kwargs with the `make` kwargs
    env_spec_kwargs = copy.deepcopy(env_spec.kwargs)
    env_spec_kwargs.update(kwargs)

    # Load the environment creator
    if env_spec.entry_point is None:
        raise error.Error(f"{env_spec.id} registered but entry_point is not specified")
    elif callable(env_spec.entry_point):
        env_creator = env_spec.entry_point
    else:
        # Assume it's a string
        env_creator = load_env_creator(env_spec.entry_point)

    # Determine if to use the rendering
    render_modes: list[str] | None = None
    if hasattr(env_creator, "metadata"):
        _check_metadata(env_creator.metadata)
        render_modes = env_creator.metadata.get("render_modes")
    render_mode = env_spec_kwargs.get("render_mode")
    apply_human_rendering = False
    apply_render_collection = False

    # If mode is not valid, try applying HumanRendering/RenderCollection wrappers
    if (
        render_mode is not None
        and render_modes is not None
        and render_mode not in render_modes
    ):
        displayable_modes = {"rgb_array", "rgb_array_list"}.intersection(render_modes)
        if render_mode == "human" and len(displayable_modes) > 0:
            logger.warn(
                "You are trying to use 'human' rendering for an environment that doesn't natively support it. "
                "The HumanRendering wrapper is being applied to your environment."
            )
            env_spec_kwargs["render_mode"] = displayable_modes.pop()
            apply_human_rendering = True
        elif (
            render_mode.endswith("_list")
            and render_mode[: -len("_list")] in render_modes
        ):
            env_spec_kwargs["render_mode"] = render_mode[: -len("_list")]
            apply_render_collection = True
        else:
            logger.warn(
                f"The environment is being initialised with render_mode={render_mode!r} "
                f"that is not in the possible render_modes ({render_modes})."
            )

    try:
        env = env_creator(**env_spec_kwargs)
    except TypeError as e:
        if (
            str(e).find("got an unexpected keyword argument 'render_mode'") >= 0
            and apply_human_rendering
        ):
            raise error.Error(
                f"You passed render_mode='human' although {env_spec.id} doesn't implement human-rendering natively. "
                "Gym tried to apply the HumanRendering wrapper but it looks like your environment is using the old "
                "rendering API, which is not supported by the HumanRendering wrapper."
            ) from e
        else:
            raise type(e)(
                f"{e} was raised from the environment creator for {env_spec.id} with kwargs ({env_spec_kwargs})"
            )

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

    # Set the minimal env spec for the environment.
    env.unwrapped.spec = EnvSpec(
        id=env_spec.id,
        entry_point=env_spec.entry_point,
        reward_threshold=env_spec.reward_threshold,
        nondeterministic=env_spec.nondeterministic,
        max_episode_steps=None,
        order_enforce=False,
        disable_env_checker=True,
        kwargs=env_spec_kwargs,
        additional_wrappers=(),
        vector_entry_point=env_spec.vector_entry_point,
    )

    # Check if pre-wrapped wrappers
    assert env.spec is not None
    num_prior_wrappers = len(env.spec.additional_wrappers)
    if (
        env_spec.additional_wrappers[:num_prior_wrappers]
        != env.spec.additional_wrappers
    ):
        for env_spec_wrapper_spec, recreated_wrapper_spec in zip(
            env_spec.additional_wrappers, env.spec.additional_wrappers
        ):
            raise ValueError(
                f"The environment's wrapper spec {recreated_wrapper_spec} is different from the saved `EnvSpec` additional wrapper {env_spec_wrapper_spec}"
            )

    # Run the environment checker as the lowest level wrapper
    if disable_env_checker is False or (
        disable_env_checker is None and env_spec.disable_env_checker is False
    ):
        env = gym.wrappers.PassiveEnvChecker(env)

    # Add the order enforcing wrapper
    if env_spec.order_enforce:
        env = gym.wrappers.OrderEnforcing(env)

    # Add the time limit wrapper
    if max_episode_steps != -1:
        if max_episode_steps is not None:
            env = gym.wrappers.TimeLimit(env, max_episode_steps)
        elif env_spec.max_episode_steps is not None:
            env = gym.wrappers.TimeLimit(env, env_spec.max_episode_steps)

    for wrapper_spec in env_spec.additional_wrappers[num_prior_wrappers:]:
        if wrapper_spec.kwargs is None:
            raise ValueError(
                f"{wrapper_spec.name} wrapper does not inherit from `gymnasium.utils.RecordConstructorArgs`, therefore, the wrapper cannot be recreated."
            )

        env = load_env_creator(wrapper_spec.entry_point)(env=env, **wrapper_spec.kwargs)

    # Add human rendering wrapper
    if apply_human_rendering:
        env = gym.wrappers.HumanRendering(env)
    elif apply_render_collection:
        env = gym.wrappers.RenderCollection(env)

    return env


def make(id: str, **kwargs) -> Env: ...


def make(id: EnvSpec, **kwargs) -> Env: ...


def make(id: Literal["CartPole-v0", "CartPole-v1"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, int]]: ...


def make(id: Literal["MountainCar-v0"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, int]]: ...


def make(id: Literal["MountainCarContinuous-v0"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, Sequence[SupportsFloat]]]: ...


def make(id: Literal["Pendulum-v1"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, Sequence[SupportsFloat]]]: ...


def make(id: Literal["Acrobot-v1"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, int]]: ...


def make(id: Literal["LunarLander-v2", "LunarLanderContinuous-v2"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, int]]: ...


def make(id: Literal["BipedalWalker-v3", "BipedalWalkerHardcore-v3"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, Sequence[SupportsFloat]]]: ...


def make(id: Literal["CarRacing-v2"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, Sequence[SupportsFloat]]]: ...


def make(id: Literal["Blackjack-v1"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, int]]: ...


def make(id: Literal["FrozenLake-v1", "FrozenLake8x8-v1"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, int]]: ...


def make(id: Literal["CliffWalking-v0"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, int]]: ...


def make(id: Literal["Taxi-v3"], **kwargs) -> Env[np.ndarray, Union[np.ndarray, int]]: ...


def make(id: Literal[
    "Reacher-v2", "Reacher-v4",
    "Pusher-v2", "Pusher-v4",
    "InvertedPendulum-v2", "InvertedPendulum-v4",
    "InvertedDoublePendulum-v2", "InvertedDoublePendulum-v4",
    "HalfCheetah-v2", "HalfCheetah-v3", "HalfCheetah-v4",
    "Hopper-v2", "Hopper-v3", "Hopper-v4",
    "Swimmer-v2", "Swimmer-v3", "Swimmer-v4",
    "Walker2d-v2", "Walker2d-v3", "Walker2d-v4",
    "Ant-v2", "Ant-v3", "Ant-v4",
    "HumanoidStandup-v2", "HumanoidStandup-v4",
    "Humanoid-v2", "Humanoid-v3", "Humanoid-v4",
], **kwargs) -> Env[np.ndarray, np.ndarray]: ...


def make(
    id: Union[str, EnvSpec],
    max_episode_steps: Optional[int] = None,
    autoreset: bool = False,
    apply_api_compatibility: Optional[bool] = None,
    disable_env_checker: Optional[bool] = None,
    **kwargs,
) -> Env:
    """Create an environment according to the given ID.

    To find all available environments use `gym.envs.registry.keys()` for all valid ids.

    Args:
        id: Name of the environment. Optionally, a module to import can be included, eg. 'module:Env-v0'
        max_episode_steps: Maximum length of an episode (TimeLimit wrapper).
        autoreset: Whether to automatically reset the environment after each episode (AutoResetWrapper).
        apply_api_compatibility: Whether to wrap the environment with the `StepAPICompatibility` wrapper that
            converts the environment step from a done bool to return termination and truncation bools.
            By default, the argument is None to which the environment specification `apply_api_compatibility` is used
            which defaults to False. Otherwise, the value of `apply_api_compatibility` is used.
            If `True`, the wrapper is applied otherwise, the wrapper is not applied.
        disable_env_checker: If to run the env checker, None will default to the environment specification `disable_env_checker`
            (which is by default False, running the environment checker),
            otherwise will run according to this parameter (`True` = not run, `False` = run)
        kwargs: Additional arguments to pass to the environment constructor.

    Returns:
        An instance of the environment.

    Raises:
        Error: If the ``id`` doesn't exist then an error is raised
    """
    if isinstance(id, EnvSpec):
        spec_ = id
    else:
        module, id = (None, id) if ":" not in id else id.split(":")
        if module is not None:
            try:
                importlib.import_module(module)
            except ModuleNotFoundError as e:
                raise ModuleNotFoundError(
                    f"{e}. Environment registration via importing a module failed. "
                    f"Check whether '{module}' contains env registration and can be imported."
                )
        spec_ = registry.get(id)

        ns, name, version = parse_env_id(id)
        latest_version = find_highest_version(ns, name)
        if (
            version is not None
            and latest_version is not None
            and latest_version > version
        ):
            logger.warn(
                f"The environment {id} is out of date. You should consider "
                f"upgrading to version `v{latest_version}`."
            )
        if version is None and latest_version is not None:
            version = latest_version
            new_env_id = get_env_id(ns, name, version)
            spec_ = registry.get(new_env_id)
            logger.warn(
                f"Using the latest versioned environment `{new_env_id}` "
                f"instead of the unversioned environment `{id}`."
            )

        if spec_ is None:
            _check_version_exists(ns, name, version)
            raise error.Error(f"No registered env with id: {id}")

    _kwargs = spec_.kwargs.copy()
    _kwargs.update(kwargs)

    if spec_.entry_point is None:
        raise error.Error(f"{spec_.id} registered but entry_point is not specified")
    elif callable(spec_.entry_point):
        env_creator = spec_.entry_point
    else:
        # Assume it's a string
        env_creator = load(spec_.entry_point)

    mode = _kwargs.get("render_mode")
    apply_human_rendering = False
    apply_render_collection = False

    # If we have access to metadata we check that "render_mode" is valid and see if the HumanRendering wrapper needs to be applied
    if mode is not None and hasattr(env_creator, "metadata"):
        assert isinstance(
            env_creator.metadata, dict
        ), f"Expect the environment creator ({env_creator}) metadata to be dict, actual type: {type(env_creator.metadata)}"

        if "render_modes" in env_creator.metadata:
            render_modes = env_creator.metadata["render_modes"]
            if not isinstance(render_modes, Sequence):
                logger.warn(
                    f"Expects the environment metadata render_modes to be a Sequence (tuple or list), actual type: {type(render_modes)}"
                )

            # Apply the `HumanRendering` wrapper, if the mode=="human" but "human" not in render_modes
            if (
                mode == "human"
                and "human" not in render_modes
                and ("rgb_array" in render_modes or "rgb_array_list" in render_modes)
            ):
                logger.warn(
                    "You are trying to use 'human' rendering for an environment that doesn't natively support it. "
                    "The HumanRendering wrapper is being applied to your environment."
                )
                apply_human_rendering = True
                if "rgb_array" in render_modes:
                    _kwargs["render_mode"] = "rgb_array"
                else:
                    _kwargs["render_mode"] = "rgb_array_list"
            elif (
                mode not in render_modes
                and mode.endswith("_list")
                and mode[: -len("_list")] in render_modes
            ):
                _kwargs["render_mode"] = mode[: -len("_list")]
                apply_render_collection = True
            elif mode not in render_modes:
                logger.warn(
                    f"The environment is being initialised with mode ({mode}) that is not in the possible render_modes ({render_modes})."
                )
        else:
            logger.warn(
                f"The environment creator metadata doesn't include `render_modes`, contains: {list(env_creator.metadata.keys())}"
            )

    if apply_api_compatibility is True or (
        apply_api_compatibility is None and spec_.apply_api_compatibility is True
    ):
        # If we use the compatibility layer, we treat the render mode explicitly and don't pass it to the env creator
        render_mode = _kwargs.pop("render_mode", None)
    else:
        render_mode = None

    try:
        env = env_creator(**_kwargs)
    except TypeError as e:
        if (
            str(e).find("got an unexpected keyword argument 'render_mode'") >= 0
            and apply_human_rendering
        ):
            raise error.Error(
                f"You passed render_mode='human' although {id} doesn't implement human-rendering natively. "
                "Gym tried to apply the HumanRendering wrapper but it looks like your environment is using the old "
                "rendering API, which is not supported by the HumanRendering wrapper."
            )
        else:
            raise e

    # Copies the environment creation specification and kwargs to add to the environment specification details
    spec_ = copy.deepcopy(spec_)
    spec_.kwargs = _kwargs
    env.unwrapped.spec = spec_

    # Add step API wrapper
    if apply_api_compatibility is True or (
        apply_api_compatibility is None and spec_.apply_api_compatibility is True
    ):
        env = EnvCompatibility(env, render_mode)

    # Run the environment checker as the lowest level wrapper
    if disable_env_checker is False or (
        disable_env_checker is None and spec_.disable_env_checker is False
    ):
        env = PassiveEnvChecker(env)

    # Add the order enforcing wrapper
    if spec_.order_enforce:
        env = OrderEnforcing(env)

    # Add the time limit wrapper
    if max_episode_steps is not None:
        env = TimeLimit(env, max_episode_steps)
    elif spec_.max_episode_steps is not None:
        env = TimeLimit(env, spec_.max_episode_steps)

    # Add the autoreset wrapper
    if autoreset:
        env = AutoResetWrapper(env)

    # Add human rendering wrapper
    if apply_human_rendering:
        env = HumanRendering(env)
    elif apply_render_collection:
        env = RenderCollection(env)

    return env


def make(
    id: str,
    num_envs: int = 1,
    asynchronous: bool = True,
    wrappers: Optional[Union[callable, List[callable]]] = None,
    disable_env_checker: Optional[bool] = None,
    **kwargs,
) -> VectorEnv:
    """Create a vectorized environment from multiple copies of an environment, from its id.

    Example::

        >>> import gym
        >>> env = gym.vector.make('CartPole-v1', num_envs=3)
        >>> env.reset()
        array([[-0.04456399,  0.04653909,  0.01326909, -0.02099827],
               [ 0.03073904,  0.00145001, -0.03088818, -0.03131252],
               [ 0.03468829,  0.01500225,  0.01230312,  0.01825218]],
              dtype=float32)

    Args:
        id: The environment ID. This must be a valid ID from the registry.
        num_envs: Number of copies of the environment.
        asynchronous: If `True`, wraps the environments in an :class:`AsyncVectorEnv` (which uses `multiprocessing`_ to run the environments in parallel). If ``False``, wraps the environments in a :class:`SyncVectorEnv`.
        wrappers: If not ``None``, then apply the wrappers to each internal environment during creation.
        disable_env_checker: If to run the env checker for the first environment only. None will default to the environment spec `disable_env_checker` parameter
            (that is by default False), otherwise will run according to this argument (True = not run, False = run)
        **kwargs: Keywords arguments applied during `gym.make`

    Returns:
        The vectorized environment.
    """

    def create_env(env_num: int):
        """Creates an environment that can enable or disable the environment checker."""
        # If the env_num > 0 then disable the environment checker otherwise use the parameter
        _disable_env_checker = True if env_num > 0 else disable_env_checker

        def _make_env():
            env = gym.envs.registration.make(
                id,
                disable_env_checker=_disable_env_checker,
                **kwargs,
            )
            if wrappers is not None:
                if callable(wrappers):
                    env = wrappers(env)
                elif isinstance(wrappers, Iterable) and all(
                    [callable(w) for w in wrappers]
                ):
                    for wrapper in wrappers:
                        env = wrapper(env)
                else:
                    raise NotImplementedError
            return env

        return _make_env

    env_fns = [
        create_env(disable_env_checker or env_num > 0) for env_num in range(num_envs)
    ]
    return AsyncVectorEnv(env_fns) if asynchronous else SyncVectorEnv(env_fns)


def make(
    reporters: dict[str, LoadedPlugin],
    options: argparse.Namespace,
) -> BaseFormatter:
    """Make the formatter from the requested user options.

    - if :option:`flake8 --quiet` is specified, return the ``quiet-filename``
      formatter.
    - if :option:`flake8 --quiet` is specified at least twice, return the
      ``quiet-nothing`` formatter.
    - otherwise attempt to return the formatter by name.
    - failing that, assume it is a format string and return the ``default``
      formatter.
    """
    format_name = options.format
    if options.quiet == 1:
        format_name = "quiet-filename"
    elif options.quiet >= 2:
        format_name = "quiet-nothing"

    try:
        format_plugin = reporters[format_name]
    except KeyError:
        LOG.warning(
            "%r is an unknown formatter.  Falling back to default.",
            format_name,
        )
        format_plugin = reporters["default"]

    return format_plugin.obj(options)

