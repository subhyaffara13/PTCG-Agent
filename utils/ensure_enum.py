
def ensure_enum(case: bool | RematCases) -> RematCases:
  if isinstance(case, bool):
    return Saveable if case else Recompute
  if not isinstance(case, (RecomputeType, SaveableType, Offloadable)):
    msg = ("Value returned by a remat policy should be a bool or"
           " `ad_checkpoint.Recompute`, `ad_checkpoint.Saveable` or"
           " `ad_checkpoint.Offloadable(...)`."
           f" Got {case} of type {type(case)}.")
    if isinstance(case, Offloadable):
      msg += ("Did you return `Offloadable` instead of an instantiated"
              " `Offloadable(...)`?")
    raise TypeError(msg)
  return case

