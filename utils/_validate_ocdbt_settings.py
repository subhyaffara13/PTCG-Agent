
def _validate_ocdbt_settings(infos: Sequence[types.ParamInfo]) -> bool:
  """Checks that all parameters have matching OCDBT flags set."""
  assert infos
  use_ocdbt = infos[0].is_ocdbt_checkpoint
  for info in infos:
    if info.is_ocdbt_checkpoint != use_ocdbt:
      raise ValueError(
          f"OCDBT settings for parameter {info.name} don't match those for the"
          f' rest of parameters: got ({info.is_ocdbt_checkpoint=}, expected'
          f' {use_ocdbt=}.'
      )
  if use_ocdbt is None:
    raise ValueError('Setting of `use_ocdbt` may not be None.')
  return use_ocdbt

