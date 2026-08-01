
def convert_to_metaty(arg):
  # TODO(yashkatariya): Remove this Tracer special case after
  # getattr(Tracer, 'sharding') is fast.
  if isinstance(arg, core.Tracer):
    return create_meta_ty(arg.aval, None, None, True, False)
  aval = core.shaped_abstractify(arg)
  arg_sharding = getattr(arg, 'sharding', None)
  arg_format = getattr(arg, 'format', None)
  arg_committed = getattr(arg, '_committed', True)
  is_np_array = isinstance(arg, np.ndarray)
  return create_meta_ty(aval, arg_sharding, arg_format, arg_committed,
                        is_np_array)

