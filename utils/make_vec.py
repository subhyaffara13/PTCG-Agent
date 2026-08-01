
def make_vec(
    id: str | EnvSpec,
    num_envs: int = 1,
    vectorization_mode: VectorizeMode | str | None = None,
    vector_kwargs: dict[str, Any] | None = None,
    wrappers: Sequence[Callable[[Env], Wrapper]] | None = None,
    **kwargs,
) -> gym.vector.VectorEnv:
    """Create a vector environment according to the given ID.

    To find all available environments use :func:`gymnasium.pprint_registry` or ``gymnasium.registry.keys()`` for all valid ids.
    We refer to the Vector environment as the vectorizor while the environment being vectorized is the base or vectorized environment (``vectorizor(vectorized env)``).

    Args:
        id: Name of the environment. Optionally, a module to import can be included, e.g. 'module:Env-v0'
        num_envs: Number of environments to create
        vectorization_mode: The vectorization method used, defaults to ``None`` such that if env id' spec has a ``vector_entry_point`` (not ``None``),
            this is first used otherwise defaults to ``sync`` to use the :class:`gymnasium.vector.SyncVectorEnv`.
            Valid modes are ``"async"``, ``"sync"`` or ``"vector_entry_point"``. Recommended to use the :class:`VectorizeMode` enum rather than strings.
        vector_kwargs: Additional arguments to pass to the vectorizor environment constructor, i.e., ``SyncVectorEnv(..., **vector_kwargs)``.
        wrappers: A sequence of wrapper functions to apply to the base environment. Can only be used in ``"sync"`` or ``"async"`` mode.
        **kwargs: Additional arguments passed to the base environment constructor.

    Returns:
        An instance of the environment.

    Raises:
        Error: If the ``id`` doesn't exist then an error is raised
    """
    if vector_kwargs is None:
        vector_kwargs = {}
    if wrappers is None:
        wrappers = []

    if isinstance(id, EnvSpec):
        env_spec = id
    elif isinstance(id, str):
        env_spec = _find_spec(id)
    else:
        raise error.Error(f"Invalid id type: {type(id)}. Expected `str` or `EnvSpec`")

    env_spec = copy.deepcopy(env_spec)
    env_spec_kwargs = env_spec.kwargs
    # for sync or async, these parameters should be passed in `make(..., **kwargs)` rather than in the env spec kwargs, therefore, we `reset` the kwargs
    env_spec.kwargs = dict()

    num_envs = env_spec_kwargs.pop("num_envs", num_envs)
    vectorization_mode = env_spec_kwargs.pop("vectorization_mode", vectorization_mode)
    vector_kwargs = env_spec_kwargs.pop("vector_kwargs", vector_kwargs)
    wrappers = env_spec_kwargs.pop("wrappers", wrappers)

    env_spec_kwargs.update(kwargs)

    # Specify the vectorization mode if None or update to a `VectorizeMode`
    if vectorization_mode is None:
        if env_spec.vector_entry_point is not None:
            vectorization_mode = VectorizeMode.VECTOR_ENTRY_POINT
        else:
            vectorization_mode = VectorizeMode.SYNC
    else:
        try:
            vectorization_mode = VectorizeMode(vectorization_mode)
        except ValueError:
            raise ValueError(
                f"Invalid vectorization mode: {vectorization_mode!r}, "
                f"valid modes: {[mode.value for mode in VectorizeMode]}"
            )
    assert isinstance(vectorization_mode, VectorizeMode)

    def create_single_env() -> Env:
        single_env = make(env_spec, **env_spec_kwargs.copy())

        if wrappers is None:
            return single_env

        for wrapper in wrappers:
            single_env = wrapper(single_env)
        return single_env

    if vectorization_mode == VectorizeMode.SYNC:
        if env_spec.entry_point is None:
            raise error.Error(
                f"Cannot create vectorized environment for {env_spec.id} because it doesn't have an entry point defined."
            )

        env = gym.vector.SyncVectorEnv(
            env_fns=(create_single_env for _ in range(num_envs)),
            **vector_kwargs,
        )
    elif vectorization_mode == VectorizeMode.ASYNC:
        if env_spec.entry_point is None:
            raise error.Error(
                f"Cannot create vectorized environment for {env_spec.id} because it doesn't have an entry point defined."
            )

        env = gym.vector.AsyncVectorEnv(
            env_fns=[create_single_env for _ in range(num_envs)],
            **vector_kwargs,
        )

    elif vectorization_mode == VectorizeMode.VECTOR_ENTRY_POINT:
        if len(vector_kwargs) > 0:
            raise error.Error(
                f"Custom vector environment can be passed arguments only through kwargs and `vector_kwargs` is not empty ({vector_kwargs})"
            )
        elif len(wrappers) > 0:
            raise error.Error(
                f"Cannot use `vector_entry_point` vectorization mode with the wrappers argument ({wrappers})."
            )
        elif len(env_spec.additional_wrappers) > 0:
            raise error.Error(
                f"Cannot use `vector_entry_point` vectorization mode with the additional_wrappers parameter in spec being not empty ({env_spec.additional_wrappers})."
            )

        entry_point = env_spec.vector_entry_point
        if entry_point is None:
            raise error.Error(
                f"Cannot create vectorized environment for {id} because it doesn't have a vector entry point defined."
            )
        elif callable(entry_point):
            env_creator = entry_point
        else:  # Assume it's a string
            env_creator = load_env_creator(entry_point)

        if (
            env_spec.max_episode_steps is not None
            and "max_episode_steps" not in env_spec_kwargs
        ):
            env_spec_kwargs["max_episode_steps"] = env_spec.max_episode_steps

        env = env_creator(num_envs=num_envs, **env_spec_kwargs)
    else:
        raise error.Error(f"Unknown vectorization mode: {vectorization_mode}")

    # Copies the environment creation specification and kwargs to add to the environment specification details
    copied_id_spec = copy.deepcopy(env_spec)
    copied_id_spec.kwargs = env_spec_kwargs.copy()
    if num_envs != 1:
        copied_id_spec.kwargs["num_envs"] = num_envs
    copied_id_spec.kwargs["vectorization_mode"] = vectorization_mode.value
    if len(vector_kwargs) > 0:
        copied_id_spec.kwargs["vector_kwargs"] = vector_kwargs
    if len(wrappers) > 0:
        copied_id_spec.kwargs["wrappers"] = wrappers
    env.unwrapped.spec = copied_id_spec

    if "autoreset_mode" not in env.metadata:
        warn(
            f"The VectorEnv ({env}) is missing AutoresetMode metadata, metadata={env.metadata}"
        )
    elif not isinstance(env.metadata["autoreset_mode"], AutoresetMode):
        warn(
            f"The VectorEnv ({env}) metadata['autoreset_mode'] is not an instance of AutoresetMode, {type(env.metadata['autoreset_mode'])}."
        )

    return env

