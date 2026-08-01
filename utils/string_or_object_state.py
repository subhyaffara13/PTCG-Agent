
def string_or_object_state(
    name: str,
    default: Any,
    help: str,
    *,
    update_global_hook: Callable[[Any], None] | None = None,
    update_thread_local_hook: Callable[[Any], None] | None = None,
    validator: Callable[[Any], None] | None = None,
    include_in_jit_key: bool = False,
    include_in_trace_context: bool = False,
) -> State[Any]:
  """Set up thread-local state and return a contextmanager for managing it.

  Similar to ``string_state``, except the context manager will accept
  any object, not just a string. Any value passed via command line flag or
  environment variable will be treated as a string.

  Args:
    name: string, converted to lowercase to define the name of the config
      option (and absl flag). It is converted to uppercase to define the
      corresponding shell environment variable.
    default: string, a default value for the option.
    help: string, used to populate the flag help information as well as the
      docstring of the returned context manager.
    update_global_hook: an optional callback that is called with the updated
      value of the global state when it is altered or set initially.
    update_thread_local_hook: an optional callback that is called with the
      updated value of the thread-local state when it is altered or set
      initially.
    validator: an optional callback that is called with the new
      value on any update, and should raise an error if the new value is
      invalid.

  Returns:
    A contextmanager to control the thread-local state value.
  """
  name = name.lower()
  default = os.getenv(name.upper(), default)
  config._contextmanager_flags.add(name)

  def parser(new_val):
    if validator is not None:
      validator(new_val)
    return new_val

  s = State[Any](
      name, default, help, update_global_hook, update_thread_local_hook,
      parser, include_in_jit_key=include_in_jit_key,
      include_in_trace_context=include_in_trace_context)
  setattr(Config, name, property(lambda _: s.value))
  config.add_option(name, s, str, meta_args=[], meta_kwargs={"help": help})
  return s

