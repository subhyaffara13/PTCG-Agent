
def bool_flag(name: str, *, default: bool, help: str) -> FlagHolder[bool]:
  """Set up a boolean flag.

  Example::

    enable_foo = bool_flag(
        name='flax_enable_foo',
        default=False,
        help='Enable foo.',
    )

  Now the ``FLAX_ENABLE_FOO`` shell environment variable can be used to
  control the process-level value of the flag, in addition to using e.g.
  ``config.update("flax_enable_foo", True)`` directly.

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
  config._add_option(name, static_bool_env(name.upper(), default))
  fh = FlagHolder[bool](name, help)
  setattr(Config, name, property(lambda _: fh.value, doc=help))
  return fh


def bool_flag(name, default, *args, **kwargs) -> Flag[bool]:
  update_hook = kwargs.pop("update_hook", None)
  holder = Flag(name, default, update_hook)
  config.add_option(name, holder, bool, args, kwargs)
  return holder

