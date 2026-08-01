
def enum_class_state(
    name: str,
    enum_class: type[_ET],
    default: _ET,
    help: str,
    *,
    update_global_hook: Callable[[_ET], None] | None = None,
    update_thread_local_hook: Callable[[_ET | None], None] | None = None,
    include_in_jit_key: bool = False,
    include_in_trace_context: bool = False,
    extra_validator: Callable[[_ET], None] | None = None,
) -> State[_ET]:
  """Set up thread-local state and return a contextmanager for managing it.

  See docstring for ``bool_state``.

  Args:
    name: string, converted to lowercase to define the name of the config
      option (and absl flag). It is converted to uppercase to define the
      corresponding shell environment variable.
    enum_class: a subtype of enum.Enum.
    default: an instance of enum_class that is the default value.
    help: string, used to populate the flag help information as well as the
      docstring of the returned context manager.
    include_in_jit_key: bool, optional: whether to include the state in the
      JIT cache key.
    include_in_trace_context: bool, optional: whether to include the state in
      the trace context.
    extra_validator: optional function to validate the value of the config
      option.

  Returns:
    A contextmanager to control the thread-local state value.
  """
  if not isinstance(default, enum_class):
    raise TypeError(
        f'Default value must be of type {enum_class}, got {default} '
        f"of type {getattr(type(default), '__name__', type(default))}"
    )
  name = name.lower()
  default_str = os.getenv(name.upper(), None)
  if default_str is not None:
    try:
      default = enum_class(default_str)
    except ValueError as e:
      raise ValueError(f"Invalid value \"{default_str}\" for JAX flag {name}") from e
  config._contextmanager_flags.add(name)

  def parser(new_val):
    if isinstance(new_val, str):
      return enum_class(new_val)
    if not isinstance(new_val, enum_class):
      raise TypeError(
          f'new enum value must be an instance of {enum_class}, got'
          f' {new_val} of type {type(new_val)}.'
      )
    if extra_validator is not None:
      extra_validator(new_val)
    return new_val

  s = State[_ET](
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
      name, s, 'enum_class',
      meta_args=[],
      meta_kwargs={"enum_class": enum_class, "help": help}
  )
  setattr(Config, name, property(lambda _: s.value))
  return s

