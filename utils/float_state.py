import os
from typing import Callable

def float_state(
    name: str,
    default: float,
    help: str,
    *,
    update_global_hook: Callable[[float], None] | None = None,
    update_thread_local_hook: Callable[[float | None], None] | None = None,
) -> State[float]:
  """Set up thread-local state and return a contextmanager for managing it.

  See docstring for ``bool_state``.

  Args:
    name: string, converted to lowercase to define the name of the config
      option (and absl flag). It is converted to uppercase to define the
      corresponding shell environment variable.
    default: default value.
    help: string, used to populate the flag help information as well as the
      docstring of the returned context manager.

  Returns:
    A contextmanager to control the thread-local state value.
  """
  if not isinstance(default, float):
    raise TypeError(f"Default value must be of type float, got {default} "
                    f"of type {getattr(type(default), '__name__', type(default))}")
  name = name.lower()
  default_env = os.getenv(name.upper())
  if default_env is not None:
    try:
      default = float(default_env)
    except ValueError:
      raise ValueError(f"Invalid value \"{default_env}\" for JAX flag {name}")
  config._contextmanager_flags.add(name)

  def parser(new_val):
    if new_val is not None and not isinstance(new_val, (float, int)):
      raise ValueError(
        f'new float config value must be None or of type float, '
        f'got {new_val} of type {type(new_val)}')
    return new_val

  s = State[float](name, default, help, update_global_hook,
                   update_thread_local_hook, parser)
  config.add_option(name, s, float, meta_args=[], meta_kwargs={"help": help})
  setattr(Config, name, property(lambda _: s.value))
  return s

