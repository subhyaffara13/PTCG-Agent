from typing import Callable

def optional_string_state(
    name: str,
    default: str | None,
    help: str,
    *,
    update_global_hook: Callable[[str], None] | None = None,
    update_thread_local_hook: Callable[[str | None], None] | None = None,
    include_in_trace_context: bool = False,
) -> State[str | None]:
  """Set up thread-local state and return a contextmanager for managing it.

  See docstring for ``bool_state``.

  Args:
    name: string, converted to lowercase to define the name of the config
      option (and absl flag). It is converted to uppercase to define the
      corresponding shell environment variable.
    default: optional string, a default value for the option.
    help: string, used to populate the flag help information as well as the
      docstring of the returned context manager.
    update_global_hook: an optional callback that is called with the updated
      value of the global state when it is altered or set initially.
    update_thread_local_hook: an optional callback that is called with the
      updated value of the thread-local state when it is altered or set
      initially.

  Returns:
    A contextmanager to control the thread-local state value.
  """
  if default is not None and not isinstance(default, str):
    raise TypeError(f"Default value must be of type str or None, got {default} "
                    f"of type {getattr(type(default), '__name__', type(default))}")

  def validator(new_val):
    if new_val is not None and not isinstance(new_val, str):
      raise ValueError('new string config value must be None or of type str,'
                       f' got {new_val} of type {type(new_val)}.')

  return string_or_object_state(
      name, default, help,
      update_global_hook=update_global_hook,
      update_thread_local_hook=update_thread_local_hook,
      validator=validator,
      include_in_trace_context=include_in_trace_context)

