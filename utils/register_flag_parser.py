
def register_flag_parser(*, parser: flags.ArgumentParser) -> Callable[[_T], _T]:
  """Creates a decorator to register parser on types.

  For example:

  ```
  class ParserForCustomConfig(flags.ArgumentParser):
  def parse(self, value):
    if isinstance(value, CustomConfig):
      return value
    return CustomConfig(i=int(value), j=int(value))


  @config_flags.register_flag_parser(parser=ParserForCustomConfig())
  @dataclasses.dataclass
  class CustomConfig:
    i: int = None
    j: int = None

  class MainConfig:
    sub: CustomConfig = CustomConfig()

  config_flags.DEFINE_config_dataclass(
    'cfg', MainConfig(), 'MyConfig data')
  ```

  will declare cfg flag, then passing `--cfg.sub=1`, will initialize
  both i and j fields to 1. The fields can still be set individually:
  `--cfg.sub=1 --cfg.sub.j=3` will set `i` to `1` and `j` to `3`.

  Args:
    parser: parser to use.

  Returns:
    Decorator to apply to types.
  """
  return ft.partial(register_flag_parser_for_type, parser=parser)

