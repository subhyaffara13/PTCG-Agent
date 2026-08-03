import os
from typing import Callable

def enum_state(
    name: str,
    enum_values: Sequence[str],
    default: str,
    help: str,
    *,
    update_global_hook: Callable[[str], None] | None = None,
    update_thread_local_hook: Callable[[str | None], None] | None = None,
    include_in_jit_key: bool = False,
    include_in_trace_context: bool = False,
    extra_validator: Callable[[str], None] | None = None,
) -> State[str]:
  """Set up thread-local state and return a contextmanager for managing it.

  See docstring for ``bool_state``.

  Args:
    name: string, converted to lowercase to define the name of the config
      option (and absl flag). It is converted to uppercase to define the
      corresponding shell environment variable.
    enum_values: list of strings representing the possible values for the
      option.
    default: string, default value.
    help: string, used to populate the flag help information as well as the
      docstring of the returned context manager.
    include_in_jit_key: bool, optional: whether to include the state in the
      JIT cache key.
    extra_validator: optional function to validate the value of the config
      option.

  Returns:
    A contextmanager to control the thread-local state value.
  """
  if not isinstance(default, str):
    raise TypeError(f"Default value must be of type str, got {default} "
                    f"of type {getattr(type(default), '__name__', type(default))}")
  name = name.lower()
  default = os.getenv(name.upper(), default)
  if default not in enum_values:
    raise ValueError(f"Invalid value \"{default}\" for JAX flag {name}")
  config._contextmanager_flags.add(name)

  def parser(new_val):
    if type(new_val) is not str or new_val not in enum_values:
      raise ValueError(f"new enum value must be in {enum_values}, "
                       f"got {new_val} of type {type(new_val)}.")
    if extra_validator is not None:
      extra_validator(new_val)
    return new_val

  s = State[str](
      name,
      default,
      help,
      update_global_hook=update_global_hook,
      update_thread_local_hook=update_thread_local_hook,
      parser=parser,
      include_in_jit_key=include_in_jit_key,
      include_in_trace_context=include_in_trace_context,
  )
  config.add_option(
      name, s, 'enum',
      meta_args=[],
      meta_kwargs={"enum_values": enum_values, "help": help}
  )
  setattr(Config, name, property(lambda _: s.value))
  return s

