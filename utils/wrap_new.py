
def wrap_new(cls: _ClsT, descriptor_infos: list[DescriptorInfo]) -> _ClsT:
  """`__new__` decorator to replace the fields by descriptors on first usage."""
  if not descriptor_infos:
    return cls
  cls._edc_processed = False  # pylint: disable=protected-access

  old_new_fn = cls.__new__

  @functools.wraps(old_new_fn)
  def new_new_fn(cls, *args, **kwargs):
    if old_new_fn is object.__new__:
      self = old_new_fn(cls)
    else:
      self = old_new_fn(cls, *args, **kwargs)

    # Already called, skipping initialization
    if cls.__dict__.get('_edc_processed'):
      return self

    # First time, apply to all parent classes .
    for curr_cls in cls.mro():  # Apply to all parent classes
      if cls.__dict__.get('_edc_processed', True):
        # Either:
        # This class is not a `@edc.dataclass` (but parent might)
        # This class is already processed
        continue

      _replace_field_by_descriptor(curr_cls, descriptor_infos=descriptor_infos)

    cls._edc_processed = True  # pylint: disable=protected-access
    return self

  cls.__new__ = new_new_fn
  return cls

