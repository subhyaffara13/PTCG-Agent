
def flagsaver(func: _CallableT) -> _CallableT:
  ...


def flagsaver(
    *args: tuple[flags.FlagHolder, Any], **kwargs: Any
) -> '_FlagOverrider':
  ...


def flagsaver(*args, **kwargs):
  """The main flagsaver interface. See module doc for usage."""
  return _construct_overrider(_FlagOverrider, *args, **kwargs)  # type: ignore[bad-return-type]

