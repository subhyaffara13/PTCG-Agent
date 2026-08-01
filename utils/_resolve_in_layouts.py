
def _resolve_in_layouts(args, jit_in_layouts, resolved_in_shardings,
                        in_avals) -> Sequence[Layout | AutoLayoutSingleton | None]:
  # If device or backend is set, return the default layout. This is because you
  # can pass arrays on cpu (with untiled layouts) to jit with backend='tpu'
  # which causes error checks to fail. Returning the default layout allows
  # this to exist. It's the same for handling shardings.
  if pxla.check_device_backend_on_shardings(resolved_in_shardings):
    return (None,) * len(jit_in_layouts)

  resolved_in_layouts: list[Layout | AutoLayoutSingleton | None] = []
  for arg, jit_in_l, rs, aval in safe_zip(
      args, jit_in_layouts, resolved_in_shardings, in_avals):
    committed = arg.committed
    # `arg_layout` is only used for checking purposes in the `else` branch
    # below. We cannot replace default layout with None to raise nicer errors.
    # `dispatch_arg_layout` replaces default layouts with `None` to simplify
    # dispatch and lowering logic downstream.
    if arg.format is not None:
      arg_layout = arg.format.layout
      dispatch_arg_layout = (None if pxla.is_default_layout(arg_layout, rs, aval)
                             else arg_layout)
    else:
      arg_layout, dispatch_arg_layout = None, None
    if jit_in_l is None:
      if committed:
        if isinstance(rs, UnspecifiedValue):
          resolved_in_layouts.append(None)
        else:
          resolved_in_layouts.append(dispatch_arg_layout)
      else:
        resolved_in_layouts.append(None)
    else:
      # arg_layout can be None because some backends don't implement the
      # required layout methods. Hence `arr.format` can return
      # `Format(None, sharding)`
      if (committed
          and not isinstance(rs, UnspecifiedValue)
          and arg_layout is not None
          and not pxla.is_user_xla_layout_equal(jit_in_l, arg_layout)):
        extra_msg = ''
        if isinstance(jit_in_l, AutoLayoutSingleton):
          extra_msg = (
              ' The layout given to `jax.jit` is `Layout.AUTO` but'
              ' the corresponding argument passed is a `jax.Array` with a'
              ' concrete layout. Consider passing a `jax.ShapeDtypeStruct`'
              ' instead of `jax.Array` as an argument to the jitted function '
              ' when using `Layout.AUTO`.'
          )
        raise ValueError('Layout passed to jit does not match the layout '
                          'on the respective arg. '
                          f'Got jit layout: {jit_in_l},\n'
                          f'arg layout: {arg_layout} for arg type: {arg.aval}.'
                          f'{extra_msg}')
      jit_in_l = (None if isinstance(jit_in_l, Layout) and
                  pxla.is_default_layout(jit_in_l, rs, aval) else jit_in_l)
      resolved_in_layouts.append(jit_in_l)
  return tuple(resolved_in_layouts)

