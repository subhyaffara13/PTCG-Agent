
def DEFINE_config_file(  # pylint: disable=g-bad-name
    name: str,
    default: Optional[str] = None,
    help_string: str = 'path to config file.',
    flag_values: flags.FlagValues = FLAGS,
    lock_config: bool = True,
    accept_new_attributes: bool = False,
    sys_argv: Optional[List[str]] = None,
    **kwargs) -> flags.FlagHolder:
  r"""Defines flag for `ConfigDict` files compatible with absl flags.

  The flag's value should be a path to a valid python file which contains a
  function called `get_config()` that returns a python object specifying
  a configuration. After the flag is parsed, `FLAGS.name` will contain
  a reference to this object, optionally with some values overridden.

  During flags parsing, every flag of form `--name.([a-zA-Z0-9]+\.?)+=value`
  and `-name.([a-zA-Z0-9]+\.?)+ value` will be treated as an override of a
  specific field in the config object returned by this flag. Field is
  essentially a dot delimited path inside the object where each path element
  has to be either an attribute or a key existing in the config object.
  For example `--my_config.field1.field2=val` means "assign value val
  to the attribute (or key) `field2` inside value of the attribute (or key)
  `field1` inside the value of `my_config` object". If there are both
  attribute and key-based access with the same name, attribute is preferred.

  Typical usage example:

  `script.py`::

    from ml_collections import config_flags

    _CONFIG = config_flags.DEFINE_config_file('my_config')

    print(_CONFIG.value)

  `config.py`::

    def get_config():
      return {
          'field1': 1,
          'field2': 'tom',
          'nested': {
              'field': 2.23,
          },
      }

  The following command::

    python script.py -- --my_config=config.py
                        --my_config.field1 8
                        --my_config.nested.field=2.1

  will print::

    {'field1': 8, 'field2': 'tom', 'nested': {'field': 2.1}}

  It is possible to parameterise the get_config function, allowing it to
  return a differently structured result for different occasions. This is
  particularly useful when setting up hyperparameter sweeps across various
  network architectures.

  `parameterised_config.py`::

    def get_config(config_string):
      possible_configs = {
          'mlp': {
              'constructor': 'snt.nets.MLP',
              'config': {
                  'output_sizes': (128, 128, 1),
              }
          },
          'lstm': {
              'constructor': 'snt.LSTM',
              'config': {
                  'hidden_size': 128,
                  'forget_bias': 1.0,
              }
          }
      }
      return possible_configs[config_string]

  If a colon is present in the command line override for the config file,
  everything to the right of the colon is passed into the get_config function.
  The following command lines will both function correctly::

    python script.py -- --my_config=parameterised_config.py:mlp
                        --my_config.config.output_sizes="(256,256,1)"


    python script.py -- --my_config=parameterised_config.py:lstm
                        --my_config.config.hidden_size=256

  The following will produce an error, as the hidden_size flag does not
  exist when the "mlp" config_string is provided::

    python script.py -- --my_config=parameterised_config.py:mlp
                        --my_config.config.hidden_size=256

  Args:
    name: Flag name, optionally including extra config after a colon.
    default: Default value of the flag (default: None).
    help_string: Help string to display when --helpfull is called. (default:
      "path to config file.")
    flag_values: FlagValues instance used for parsing. (default:
      absl.flags.FLAGS)
    lock_config: If set to True, loaded config will be locked through calling
      .lock() method on its instance (if it exists). (default: True)
    accept_new_attributes: If `True`, accept to pass arbitrary attributes that
      are not originally defined in the `get_config()` dict.
      `accept_new_attributes` requires `lock_config=False`.
    sys_argv: If set, interprets this as the full list of args used in parsing.
      This is used to identify which overrides to define as flags. If not
      specified, uses the system sys.argv to figure it out.
    **kwargs: Optional keyword arguments passed to Flag constructor.

  Returns:
    a handle to defined flag.
  """
  if accept_new_attributes and lock_config:
    raise ValueError('`accept_new_attributes=True` requires lock_config=False')
  parser = ConfigFileFlagParser(name=name, lock_config=lock_config)
  serializer = flags.ArgumentSerializer()
  flag = _ConfigFlag(
      parser=parser,
      serializer=serializer,
      name=name,
      default=default,
      help_string=help_string,
      flag_values=flag_values,
      accept_new_attributes=accept_new_attributes,
      sys_argv=sys_argv,
      **kwargs)

  return flags.DEFINE_flag(flag, flag_values)

