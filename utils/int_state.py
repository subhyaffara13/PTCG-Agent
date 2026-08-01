
def int_state(
    name: str,
    default: int,
    help: str,
    *,
    update_global_hook: Callable[[int], None] | None = None,
    update_thread_local_hook: Callable[[int | None], None] | None = None,
    include_in_jit_key: bool = False,
    include_in_trace_context: bool = False,
    validator: Callable[[Any], None] | None = None,
) -> State[int]:
  """Set up thread-local state and return a contextmanager for managing it.

  See docstring for ``bool_state``.

  Args:
    name: string, converted to lowercase to define the name of the config
      option (and absl flag). It is converted to uppercase to define the
      corresponding shell environment variable.
    default: optional int, default value.
    help: string, used to populate the flag help information as well as the
      docstring of the returned context manager.

  Returns:
    A contextmanager to control the thread-local state value.
  """
  if not isinstance(default, int):
    raise TypeError(f"Default value must be of type int, got {default} "
                    f"of type {getattr(type(default), '__name__', type(default))}")
  name = name.lower()
  default_env = os.getenv(name.upper())
  if default_env is not None:
    try:
      default = int(default_env)
    except ValueError:
      raise ValueError(f"Invalid value \"{default_env}\" for JAX flag {name}")
  config._contextmanager_flags.add(name)

  def parser(new_val):
    if new_val is not None and not isinstance(new_val, int):
      raise ValueError(f'new int config value must be None or of type int, '
                       f'got {new_val} of type {type(new_val)}')
    if new_val is not None and validator is not None:
      validator(new_val)
    return new_val

  s = State[int](name, default, help, update_global_hook,
                 update_thread_local_hook, parser,
                 include_in_jit_key=include_in_jit_key,
                 include_in_trace_context=include_in_trace_context)
  config.add_option(name, s, int, meta_args=[], meta_kwargs={"help": help})
  setattr(Config, name, property(lambda _: s.value))
  return s

