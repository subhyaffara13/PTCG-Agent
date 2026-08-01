
def _graph_updates_scan(
  f, f_unbound, *,
  in_axes, out_axes,
  length, reverse, unroll, _split_transpose,
  transform_metadata,
):
  input_carry_argnum = _get_carry_argnum(in_axes, is_in_axes=True)
  output_carry_argnum = _get_carry_argnum(out_axes, is_in_axes=False)

  if (input_carry_argnum is None and output_carry_argnum is not None) or (
    input_carry_argnum is not None and output_carry_argnum is None
  ):
    raise ValueError(
      'If one of in_axes or out_axes has Carry, the other must also have Carry. '
      f'Got {in_axes=!r} and {out_axes=!r}'
    )

  scan_fn = ScanFn(
    f_unbound,
    input_carry_argnum,
    output_carry_argnum,
    in_axes,
    out_axes,
    transform_metadata,
  )

  @functools.wraps(f)
  @graphlib.update_context('scan')
  def scan_wrapper(*args, **kwargs):
    args = resolve_kwargs(f, args, kwargs)

    if in_axes is Carry and len(args) != 1:
      raise ValueError(
        f'When in_axes=Carry, the function must take exactly one argument, '
        f'got {len(args)} arguments.'
      )

    graphdefs_deque = PytreeDeque()
    carry_deque = PytreeDeque()
    broadcast_deque = PytreeDeque()
    broadcast_arrays = PytreeDeque()
    pure_args: tuple = extract.to_tree(
      args,
      prefix=in_axes,
      split_fn=functools.partial(
        _scan_split_in, carry_deque, graphdefs_deque, broadcast_deque, broadcast_arrays
      ),
      map_non_graph_nodes=True,
      ctxtag='scan',
    )
    if isinstance(input_carry_argnum, int):
      pure_carry_arg = pure_args[input_carry_argnum]
      pure_args = extract.replace_at(pure_args, input_carry_argnum, None)
    elif input_carry_argnum == 'all':
      pure_carry_arg = pure_args[0]
      pure_args = ()
    else:
      assert input_carry_argnum is None
      pure_carry_arg = None

    carry = (pure_carry_arg, carry_deque, broadcast_deque, broadcast_arrays)
    scan_in = (graphdefs_deque, pure_args)

    carry_out, scan_out = jax.lax.scan(
      scan_fn,
      carry,
      scan_in,
      length=length,
      reverse=reverse,
      unroll=unroll,
      _split_transpose=_split_transpose,
    )
    (
        pure_carry_arg_out,
        carry_deque_out,
        broadcast_deque_out,
        broadcast_arrays_out,
    ) = carry_out
    (
      graphdefs_out,
      pure_args_out,
      pure_out,
    ) = scan_out

    if input_carry_argnum == 'all':
      pure_args_out = (pure_carry_arg_out,)
    elif isinstance(input_carry_argnum, int):
      pure_args_out = extract.replace_at(pure_args_out, input_carry_argnum, pure_carry_arg_out)
    else:
      assert input_carry_argnum is None
      assert pure_carry_arg_out is None

    args_out, out = extract.from_tree(
      (pure_args_out, pure_out),
      prefix=(in_axes, out_axes),
      merge_fn=functools.partial(
        _scan_merge_out, carry_deque_out, graphdefs_out, broadcast_deque_out
      ),
      is_leaf=lambda x: isinstance(x, (extract.NodeStates, Broadcasted)),
      map_non_graph_nodes=True,
      ctxtag='scan',
      is_inner=False,
    )

    if input_carry_argnum == 'all':
      carry_arg = args_out[0]
    elif isinstance(input_carry_argnum, int):
      carry_arg = args_out[input_carry_argnum]
    else:
      assert input_carry_argnum is None
      carry_arg = None

    if output_carry_argnum == 'all':
      out = carry_arg
    elif isinstance(output_carry_argnum, int):
      out = extract.replace_at(out, output_carry_argnum, carry_arg)
    else:
      assert output_carry_argnum is None
      assert carry_arg is None

    return out

  return scan_wrapper

