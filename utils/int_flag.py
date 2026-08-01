
def int_flag(name: str, *, default: int | None, help: str) -> FlagHolder[int]:
  """Set up an integer flag.

  Example::

    num_foo = int_flag(
        name='flax_num_foo',
        default=42,
        help='Number of foo.',
    )

  Now the ``FLAX_NUM_FOO`` shell environment variable can be used to
  control the process-level value of the flag, in addition to using e.g.
  ``config.update("flax_num_foo", 42)`` directly.

  Args:
    name: converted to lowercase to define the name of the flag. It is
      converted to uppercase to define the corresponding shell environment
      variable.
    default: a default value for the flag.
    help: used to populate the docstring of the returned flag holder object.

  Returns:
    A flag holder object for accessing the value of the flag.
  """
  name = name.lower()
  config._add_option(name, static_int_env(name.upper(), default))
  fh = FlagHolder[int](name, help)
  setattr(Config, name, property(lambda _: fh.value, doc=help))
  return fh


def int_flag(name, default, *args, **kwargs) -> Flag[int]:
  update_hook = kwargs.pop("update_hook", None)
  holder = Flag(name, default, update_hook)
  config.add_option(name, holder, int, args, kwargs)
  return holder

