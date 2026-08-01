
def finalize_arg_sharding(arg_s, committed):
  if isinstance(arg_s, UnspecifiedValue):
    return arg_s
  else:
    if committed:
      return arg_s
    else:
      assert isinstance(arg_s, Sharding)
      if arg_s.num_devices == 1:
        return UNSPECIFIED
      raise NotImplementedError('Having uncommitted Array sharded on '
                                'multiple devices is not supported.')

