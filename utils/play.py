from typing import Callable, Dict, List, Optional, Tuple, Union

def play(board, column, mark, config):
    columns = config.columns
    rows = config.rows
    row = max([r for r in range(rows) if board[column + (r * columns)] == EMPTY])
    board[column + (row * columns)] = mark


def play(
    env: Env,
    transpose: bool | None = True,
    fps: int | None = None,
    zoom: float | None = None,
    callback: Callable | None = None,
    keys_to_action: dict[tuple[str | int, ...] | str | int, ActType] | None = None,
    seed: int | None = None,
    noop: ActType = 0,
    wait_on_player: bool = False,
):
    """Allows the user to play the environment using a keyboard.

    If playing in a turn-based environment, set wait_on_player to True.

    Args:
        env: Environment to use for playing.
        transpose: If this is ``True``, the output of observation is transposed. Defaults to ``True``.
        fps: Maximum number of steps of the environment executed every second. If ``None`` (the default),
            ``env.metadata["render_fps""]`` (or 30, if the environment does not specify "render_fps") is used.
        zoom: Zoom the observation in, ``zoom`` amount, should be positive float
        callback: If a callback is provided, it will be executed after every step. It takes the following input:

            * obs_t: observation before performing action
            * obs_tp1: observation after performing action
            * action: action that was executed
            * rew: reward that was received
            * terminated: whether the environment is terminated or not
            * truncated: whether the environment is truncated or not
            * info: debug info
        keys_to_action:  Mapping from keys pressed to action performed.
            Different formats are supported: Key combinations can either be expressed as a tuple of unicode code
            points of the keys, as a tuple of characters, or as a string where each character of the string represents
            one key.
            For example if pressing 'w' and space at the same time is supposed
            to trigger action number 2 then ``key_to_action`` dict could look like this:

                >>> key_to_action = {
                ...    # ...
                ...    (ord('w'), ord(' ')): 2
                ...    # ...
                ... }

            or like this:

                >>> key_to_action = {
                ...    # ...
                ...    ("w", " "): 2
                ...    # ...
                ... }

            or like this:

                >>> key_to_action = {
                ...    # ...
                ...    "w ": 2
                ...    # ...
                ... }

            If ``None``, default ``key_to_action`` mapping for that environment is used, if provided.
        seed: Random seed used when resetting the environment. If None, no seed is used.
        noop: The action used when no key input has been entered, or the entered key combination is unknown.
        wait_on_player: Play should wait for a user action

    Example:
        >>> import gymnasium as gym
        >>> import numpy as np
        >>> from gymnasium.utils.play import play
        >>> play(gym.make("CarRacing-v3", render_mode="rgb_array"),  # doctest: +SKIP
        ...     keys_to_action={
        ...         "w": np.array([0, 0.7, 0], dtype=np.float32),
        ...         "a": np.array([-1, 0, 0], dtype=np.float32),
        ...         "s": np.array([0, 0, 1], dtype=np.float32),
        ...         "d": np.array([1, 0, 0], dtype=np.float32),
        ...         "wa": np.array([-1, 0.7, 0], dtype=np.float32),
        ...         "dw": np.array([1, 0.7, 0], dtype=np.float32),
        ...         "ds": np.array([1, 0, 1], dtype=np.float32),
        ...         "as": np.array([-1, 0, 1], dtype=np.float32),
        ...     },
        ...     noop=np.array([0, 0, 0], dtype=np.float32)
        ... )

        Above code works also if the environment is wrapped, so it's particularly useful in
        verifying that the frame-level preprocessing does not render the game
        unplayable.

        If you wish to plot real time statistics as you play, you can use
        :class:`PlayPlot`. Here's a sample code for plotting the reward
        for last 150 steps.

        >>> from gymnasium.utils.play import PlayPlot, play
        >>> def callback(obs_t, obs_tp1, action, rew, terminated, truncated, info):
        ...        return [rew,]
        >>> plotter = PlayPlot(callback, 150, ["reward"])             # doctest: +SKIP
        >>> play(gym.make("CartPole-v1"), callback=plotter.callback)  # doctest: +SKIP
    """
    env.reset(seed=seed)

    if keys_to_action is None:
        if env.has_wrapper_attr("get_keys_to_action"):
            keys_to_action = env.get_wrapper_attr("get_keys_to_action")()
        else:
            assert env.spec is not None
            raise MissingKeysToAction(
                f"{env.spec.id} does not have explicit key to action mapping, "
                "please specify one manually"
            )

    assert keys_to_action is not None

    # validate the `keys_to_action` set provided
    assert isinstance(keys_to_action, dict)
    for key, action in keys_to_action.items():
        if isinstance(key, tuple):
            assert len(key) > 0
            assert all(isinstance(k, (str, int)) for k in key)
        else:
            assert isinstance(key, (str, int))

        assert action in env.action_space

    key_code_to_action = {}
    for key_combination, action in keys_to_action.items():
        if isinstance(key_combination, int):
            key_combination = (key_combination,)
        key_code = tuple(
            sorted(ord(key) if isinstance(key, str) else key for key in key_combination)
        )
        key_code_to_action[key_code] = action

    game = PlayableGame(env, key_code_to_action, zoom)

    if fps is None:
        fps = env.metadata.get("render_fps", 30)

    done, obs = True, None
    clock = pygame.time.Clock()

    while game.running:
        if done:
            done = False
            obs = env.reset(seed=seed)
        elif wait_on_player is False or len(game.pressed_keys) > 0:
            action = key_code_to_action.get(tuple(sorted(game.pressed_keys)), noop)
            prev_obs = obs
            obs, rew, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            if callback is not None:
                callback(prev_obs, obs, action, rew, terminated, truncated, info)
        if obs is not None:
            rendered = env.render()
            if isinstance(rendered, list):
                rendered = rendered[-1]
            assert rendered is not None and isinstance(rendered, np.ndarray)
            display_arr(
                game.screen, rendered, transpose=transpose, video_size=game.video_size
            )

        # process pygame events
        for event in pygame.event.get():
            game.process_event(event)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()


def play(
    env: Env,
    transpose: Optional[bool] = True,
    fps: Optional[int] = None,
    zoom: Optional[float] = None,
    callback: Optional[Callable] = None,
    keys_to_action: Optional[Dict[Union[Tuple[Union[str, int]], str], ActType]] = None,
    seed: Optional[int] = None,
    noop: ActType = 0,
):
    """Allows one to play the game using keyboard.

    Example::

        >>> import gym
        >>> from gym.utils.play import play
        >>> play(gym.make("CarRacing-v1", render_mode="rgb_array"), keys_to_action={
        ...                                                "w": np.array([0, 0.7, 0]),
        ...                                                "a": np.array([-1, 0, 0]),
        ...                                                "s": np.array([0, 0, 1]),
        ...                                                "d": np.array([1, 0, 0]),
        ...                                                "wa": np.array([-1, 0.7, 0]),
        ...                                                "dw": np.array([1, 0.7, 0]),
        ...                                                "ds": np.array([1, 0, 1]),
        ...                                                "as": np.array([-1, 0, 1]),
        ...                                               }, noop=np.array([0,0,0]))


    Above code works also if the environment is wrapped, so it's particularly useful in
    verifying that the frame-level preprocessing does not render the game
    unplayable.

    If you wish to plot real time statistics as you play, you can use
    :class:`gym.utils.play.PlayPlot`. Here's a sample code for plotting the reward
    for last 150 steps.

        >>> def callback(obs_t, obs_tp1, action, rew, terminated, truncated, info):
        ...        return [rew,]
        >>> plotter = PlayPlot(callback, 150, ["reward"])
        >>> play(gym.make("ALE/AirRaid-v5"), callback=plotter.callback)


    Args:
        env: Environment to use for playing.
        transpose: If this is ``True``, the output of observation is transposed. Defaults to ``True``.
        fps: Maximum number of steps of the environment executed every second. If ``None`` (the default),
            ``env.metadata["render_fps""]`` (or 30, if the environment does not specify "render_fps") is used.
        zoom: Zoom the observation in, ``zoom`` amount, should be positive float
        callback: If a callback is provided, it will be executed after every step. It takes the following input:
                obs_t: observation before performing action
                obs_tp1: observation after performing action
                action: action that was executed
                rew: reward that was received
                terminated: whether the environment is terminated or not
                truncated: whether the environment is truncated or not
                info: debug info
        keys_to_action:  Mapping from keys pressed to action performed.
            Different formats are supported: Key combinations can either be expressed as a tuple of unicode code
            points of the keys, as a tuple of characters, or as a string where each character of the string represents
            one key.
            For example if pressing 'w' and space at the same time is supposed
            to trigger action number 2 then ``key_to_action`` dict could look like this:
                >>> {
                ...    # ...
                ...    (ord('w'), ord(' ')): 2
                ...    # ...
                ... }
            or like this:
                >>> {
                ...    # ...
                ...    ("w", " "): 2
                ...    # ...
                ... }
            or like this:
                >>> {
                ...    # ...
                ...    "w ": 2
                ...    # ...
                ... }
            If ``None``, default ``key_to_action`` mapping for that environment is used, if provided.
        seed: Random seed used when resetting the environment. If None, no seed is used.
        noop: The action used when no key input has been entered, or the entered key combination is unknown.
    """
    env.reset(seed=seed)

    if keys_to_action is None:
        if hasattr(env, "get_keys_to_action"):
            keys_to_action = env.get_keys_to_action()
        elif hasattr(env.unwrapped, "get_keys_to_action"):
            keys_to_action = env.unwrapped.get_keys_to_action()
        else:
            raise MissingKeysToAction(
                f"{env.spec.id} does not have explicit key to action mapping, "
                "please specify one manually"
            )
    assert keys_to_action is not None

    key_code_to_action = {}
    for key_combination, action in keys_to_action.items():
        key_code = tuple(
            sorted(ord(key) if isinstance(key, str) else key for key in key_combination)
        )
        key_code_to_action[key_code] = action

    game = PlayableGame(env, key_code_to_action, zoom)

    if fps is None:
        fps = env.metadata.get("render_fps", 30)

    done, obs = True, None
    clock = pygame.time.Clock()

    while game.running:
        if done:
            done = False
            obs = env.reset(seed=seed)
        else:
            action = key_code_to_action.get(tuple(sorted(game.pressed_keys)), noop)
            prev_obs = obs
            obs, rew, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            if callback is not None:
                callback(prev_obs, obs, action, rew, terminated, truncated, info)
        if obs is not None:
            rendered = env.render()
            if isinstance(rendered, List):
                rendered = rendered[-1]
            assert rendered is not None and isinstance(rendered, np.ndarray)
            display_arr(
                game.screen, rendered, transpose=transpose, video_size=game.video_size
            )

        # process pygame events
        for event in pygame.event.get():
            game.process_event(event)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

