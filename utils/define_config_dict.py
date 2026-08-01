
def DEFINE_config_dict(  # pylint: disable=g-bad-name
    name: str,
    config: config_dict.ConfigDict,
    help_string: str = 'ConfigDict instance.',
    flag_values: flags.FlagValues = FLAGS,
    lock_config: bool = True,
    accept_new_attributes: bool = False,
    sys_argv: Optional[List[str]] = None,
    **kwargs) -> flags.FlagHolder:
  """Defines flag for inline `ConfigDict's` compatible with absl flags.

  Similar to `DEFINE_config_file` except the flag's value should be a
  `ConfigDict` instead of a path to a file containing a `ConfigDict`. After the
  flag is parsed, `FLAGS.name` will contain a reference to the `ConfigDict`,
  optionally with some values overridden.

  Typical usage example:

  `script.py`::

    from ml_collections import config_dict
    from ml_collections import config_flags


    config = config_dict.ConfigDict({
        'field1': 1,
        'field2': 'tom',
        'nested': {
            'field': 2.23,
        }
    })


    _CONFIG = config_flags.DEFINE_config_dict('my_config', config)
    ...

    print(_CONFIG.value)

  The following command::

    python script.py -- --my_config.field1 8
                        --my_config.nested.field=2.1

  will print::

    field1: 8
    field2: tom
    nested: {field: 2.1}

  Args:
    name: Flag name.
    config: `ConfigDict` object.
    help_string: Help string to display when --helpfull is called.
        (default: "ConfigDict instance.")
    flag_values: FlagValues instance used for parsing.
        (default: absl.flags.FLAGS)
    lock_config: If set to True, loaded config will be locked through calling
        .lock() method on its instance (if it exists). (default: True)
    accept_new_attributes: If `True`, accept to pass arbitrary attributes that
      are not originally defined in the `config` argument.
      `accept_new_attributes` requires `lock_config=False`.
    sys_argv: If set, interprets this as the full list of args used in parsing.
      This is used to identify which overrides to define as flags. If not
      specified, uses the system sys.argv to figure it out.
    **kwargs: Optional keyword arguments passed to Flag constructor.

  Returns:
    a handle to defined flag.
  """
  if not isinstance(config, config_dict.ConfigDict):
    raise TypeError('config should be a ConfigDict')
  if accept_new_attributes and lock_config:
    raise ValueError('`accept_new_attributes=True` requires lock_config=False')
  parser = _InlineConfigParser(name=name, lock_config=lock_config)
  flag = _ConfigFlag(
      parser=parser,
      serializer=flags.ArgumentSerializer(),
      name=name,
      default=config,
      help_string=help_string,
      flag_values=flag_values,
      accept_new_attributes=accept_new_attributes,
      sys_argv=sys_argv,
      **kwargs)

  # Get the module name for the frame at depth 1 in the call stack.
  module_name = sys._getframe(1).f_globals.get('__name__', None)  # pylint: disable=protected-access
  module_name = sys.argv[0] if module_name == '__main__' else module_name
  return flags.DEFINE_flag(flag, flag_values, module_name=module_name)

