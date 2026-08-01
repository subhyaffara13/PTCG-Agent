
def DEFINE_config_dataclass(  # pylint: disable=invalid-name
    name: str,
    config: _T,
    help_string: str = 'Configuration object. Must be a dataclass.',
    flag_values: flags.FlagValues = FLAGS,
    sys_argv: Optional[List[str]] = None,
    parse_fn: Optional[Callable[[Any], _T]] = None,
    **kwargs,
) -> flags.FlagHolder[_T]:
  """Defines a typed (dataclass) flag-overrideable configuration.

  Similar to `DEFINE_config_dict` except `config` should be a `dataclass`.

  The config value can contain nested fields, including other dataclasses.
  If a field is of form  Optional[dataclass] with None as a default value,
  it can be explicitly initialized using special value `build`. E.g.
  For instance:

  ```
  @dc.dataclass
  class FancyLoss
    foo_scale: float = 0.1

  @dc.dataclass
  class Config:
    fancy_loss: Optional[FancyLoss] = None
  ```

  Then if `--config.fancy_loss=build  --config.fancy_loss.foo_scale=1` will
  instantiate and override foo_scale to 1.  Note: that the reverse
  order is not allowed:  `--config.fancy_loss.foo_scale=1
  --config.fancy_loss=build` will cause FlagOrderError.

  Optional dataclass fields can also be set to None using special `none` value.
  For instance:

  ```
  @dc.dataclass
  class FancyLossConfig
    foo_loss_scale: float = 0.1

  @dc.dataclass
  class Config:
    fancy_loss: Optional[FancyLossConfig] = FancyLossConfig()
  ```

  Then `--config.fancy_loss=none`, will set it to None.

  Implementation note: This flag will register all the needed nested flags
  dynamically based on sys.argv or sys_argv, in order to support
  free-text keyed flags such as `foo.bar['i']=1`. Because of how flag subsystem
  works this will happen either at flag-parsing time (during app.run),
  if there is a root level override, such as `--config=<..>` or during
  declaration otherwise (during this invocation).
  Parsing at declaration (e.g. if no root override) can cause problems
  with multiprocessing  since sys.argv is not yet populated at
  declaration time for spawn processes. To avoid this, pass custom sys_argv
  value instead if you want to use this library with multiprocessing.
  Also note, in the future we might consider to always do it at declaration
  time, as this cleans up the logic significantly.

  Args:
    name: Flag name.
    config: A user-defined configuration object. Must be built via `dataclass`.
    help_string: Help string to display when --helpfull is called.
    flag_values: FlagValues instance used for parsing.
    sys_argv: If set, interprets this as the full list of args used in parsing.
      This is used to identify which overrides to define as flags. If not
      specified, uses the system sys.argv to figure it out.
    parse_fn: Function that can parse provided flag value, when assigned via
      flag.value, or passed on command line. If not provided, but the class has
      registered parser register_flag_parser_for_type, the latter will be used.
      Otherwise only allows to assign instances of this class.
    **kwargs: Optional keyword arguments passed to Flag constructor.

  Returns:
    A handle to the defined flag.
  """

  if not dataclasses.is_dataclass(config):
    raise ValueError('Configuration object must be a `dataclass`.')
  # Define the flag.
  parser = _DataclassParser(name=name, dataclass_type=type(config),
                            parse_fn=parse_fn)
  flag = _ConfigFlag(
      flag_values=flag_values,
      parser=parser,
      serializer=flags.ArgumentSerializer(),
      name=name,
      default=config,
      help_string=help_string,
      sys_argv=sys_argv,
      **kwargs)

  return flags.DEFINE_flag(flag, flag_values)

