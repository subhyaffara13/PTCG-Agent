
def unpack_as(any_msg: Any, message_type: type[_MessageT]) -> _MessageT:
  unpacked = message_type()
  if unpack(any_msg, unpacked):
    return unpacked
  else:
    raise TypeError(
        f'Attempted to unpack {type_name(any_msg)} to'
        f' {message_type.__qualname__}'
    )

