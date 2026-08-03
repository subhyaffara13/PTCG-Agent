import sys
from typing import Any, Callable

def _async_worker(
    index: int,
    env_fn: Callable,
    pipe: Connection,
    parent_pipe: Connection,
    shared_memory: SynchronizedArray | dict[str, Any] | tuple[Any, ...],
    error_queue: Queue,
    autoreset_mode: AutoresetMode,
):
    env = env_fn()
    observation_space = env.observation_space
    action_space = env.action_space
    autoreset = False
    observation = None

    parent_pipe.close()

    try:
        while True:
            command, data = pipe.recv()

            if command == "reset":
                observation, info = env.reset(**data)
                if shared_memory:
                    write_to_shared_memory(
                        observation_space, index, observation, shared_memory
                    )
                    observation = None
                    autoreset = False
                pipe.send(((observation, info), True))
            elif command == "reset-noop":
                pipe.send(((observation, {}), True))
            elif command == "step":
                if autoreset_mode == AutoresetMode.NEXT_STEP:
                    if autoreset:
                        observation, info = env.reset()
                        reward, terminated, truncated = 0, False, False
                    else:
                        (
                            observation,
                            reward,
                            terminated,
                            truncated,
                            info,
                        ) = env.step(data)
                    autoreset = terminated or truncated
                elif autoreset_mode == AutoresetMode.SAME_STEP:
                    (
                        observation,
                        reward,
                        terminated,
                        truncated,
                        info,
                    ) = env.step(data)

                    if terminated or truncated:
                        reset_observation, reset_info = env.reset()

                        info = {
                            "final_info": info,
                            "final_obs": observation,
                            **reset_info,
                        }
                        observation = reset_observation
                elif autoreset_mode == AutoresetMode.DISABLED:
                    assert autoreset is False
                    (
                        observation,
                        reward,
                        terminated,
                        truncated,
                        info,
                    ) = env.step(data)
                else:
                    raise ValueError(f"Unexpected autoreset_mode: {autoreset_mode}")

                if shared_memory:
                    write_to_shared_memory(
                        observation_space, index, observation, shared_memory
                    )
                    observation = None

                pipe.send(((observation, reward, terminated, truncated, info), True))
            elif command == "close":
                pipe.send((None, True))
                break
            elif command == "_call":
                name, args, kwargs = data
                if name in ["reset", "step", "close", "_setattr", "_check_spaces"]:
                    raise ValueError(
                        f"Trying to call function `{name}` with `call`, use `{name}` directly instead."
                    )

                attr = env.get_wrapper_attr(name)
                if callable(attr):
                    pipe.send((attr(*args, **kwargs), True))
                else:
                    pipe.send((attr, True))
            elif command == "_setattr":
                name, value = data
                env.set_wrapper_attr(name, value)
                pipe.send((None, True))
            elif command == "_check_spaces":
                obs_mode, single_obs_space, single_action_space = data

                pipe.send(
                    (
                        (
                            (
                                single_obs_space == observation_space
                                if obs_mode == "same"
                                else is_space_dtype_shape_equiv(
                                    single_obs_space, observation_space
                                )
                            ),
                            single_action_space == action_space,
                        ),
                        True,
                    )
                )
            else:
                raise RuntimeError(
                    f"Received unknown command `{command}`. Must be one of [`reset`, `step`, `close`, `_call`, `_setattr`, `_check_spaces`]."
                )
    except (KeyboardInterrupt, Exception):
        error_type, error_message, _ = sys.exc_info()
        trace = traceback.format_exc()

        error_queue.put((index, error_type, error_message, trace))
        pipe.send((None, False))
    finally:
        env.close()

