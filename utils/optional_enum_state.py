
def optional_enum_state(
    name: str,
    enum_values: Sequence[str],
    default: str | None,
    help: str,
    *,
    update_global_hook: Callable[[str | None], None] | None = None,
    update_thread_local_hook: Callable[[str | None], None] | None = None,
    include_in_jit_key: bool = False,
    include_in_trace_context: bool = False,
) -> State[str | None]:
  """Set up thread-local state and return a contextmanager for managing it.

  See docstring for ``bool_state``.

  Args:
    name: string, converted to lowercase to define the name of the config
      option (and absl flag). It is converted to uppercase to define the
      corresponding shell environment variable.
    enum_values: list of strings representing the possible values for the
      option.
    default: optional string, default value.
    help: string, used to populate the flag help information as well as the
      docstring of the returned context manager.

  Returns:
    A contextmanager to control the thread-local state value.
  """
  if default is not None and not isinstance(default, str):
    raise TypeError(f"Default value must be of type str or None, got {default} "
                    f"of type {getattr(type(default), '__name__', type(default))}")
  name = name.lower()
  default = os.getenv(name.upper(), default)
  if default is not None and default not in enum_values:
    raise ValueError(f"Invalid value \"{default}\" for JAX flag {name}")
  config._contextmanager_flags.add(name)

  def parser(new_val):
    if (new_val is not None and
      (type(new_val) is not str or new_val not in enum_values)):
      raise ValueError(f"new enum value must be None or in {enum_values}, "
                       f"got {new_val} of type {type(new_val)}.")
    return new_val

  s = State[str | None](
      name, default, help, update_global_hook, update_thread_local_hook,
      parser, include_in_jit_key=include_in_jit_key,
      include_in_trace_context=include_in_trace_context,
  )
  config.add_option(
      name, s, 'enum',
      meta_args=[],
      meta_kwargs={"enum_values": enum_values, "help": help}
  )
  setattr(Config, name, property(lambda _: s.value))
  return s

