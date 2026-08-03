import functools

def _simple_scan(
  f, f_unbound, *,
  graph, in_axes, out_axes,
  length, reverse, unroll, _split_transpose,
):
  _validate_scan_axes(in_axes, out_axes)

  out_is_tuple = isinstance(out_axes, tuple)
  was_carry = in_axes is Carry
  if in_axes is Carry:
    in_axes = (Carry,)
  if isinstance(in_axes, tuple):
    carry_arg_index = extract.find(in_axes, Carry)
    _, sliced_in_axes = extract.slice_at(in_axes, carry_arg_index)
  else:
    carry_arg_index = None
    sliced_in_axes = in_axes

  if isinstance(out_axes, tuple):
    carry_out_index = extract.find(out_axes, Carry)
    _, sliced_out_axes = extract.slice_at(out_axes, carry_out_index)
  else:
    carry_out_index = None
    sliced_out_axes = out_axes

  simple_scan_fn = SimpleScanFn(
      f_unbound, graph=graph,
      in_axes=in_axes, out_axes=out_axes,
      out_is_tuple=out_is_tuple,
      carry_arg_index=carry_arg_index,
      carry_out_index=carry_out_index,
  )

  @functools.wraps(f)
  def simple_scan_wrapper(*args):
    args = resolve_kwargs(f, args, {})
    if was_carry and len(args) != 1:
      raise ValueError(
          'When in_axes=Carry, the function must take exactly one argument, '
          f'got {len(args)} arguments.'
      )
    if graph:
      # check consistent aliasing, temporarily convert args to tree
      # to check aliasing, but the real tree convertion is done later
      check_args = extract.to_tree2(args, prefix=in_axes)
    else:
      check_args = args

    extract.check_no_aliases('scan', args=check_args)
    carry, x_args = extract.slice_at(args, carry_arg_index)

    if graph:
      # convert the carry to tree separately to ensure a consistent
      # graph structure for the carry in and carry out
      carry = extract.to_tree2(carry)
      x_args = extract.to_tree2(x_args)

    def extract_broadcasts(path, prefix_leaf, leaf):
      return leaf is not None and (
          prefix_leaf is None
          or (
              isinstance(prefix_leaf, variablelib.Variable)
              and prefix_leaf.get_value() is None
          )
      )
    x_args, broadcasts = extract.extract(
        extract_broadcasts, sliced_in_axes, x_args,
        is_leaf=lambda x: x is None or isinstance(x, variablelib.Variable),
    )

    x_args_transposed = _move_axis(
        lambda ax, leaf: jnp.moveaxis(leaf, ax, 0),
        sliced_in_axes, x_args,
    )

    (carry_out, final_broadcasts), (ys, updates) = jax.lax.scan(
        simple_scan_fn,
        (carry, broadcasts),
        x_args_transposed,
        length=length,
        reverse=reverse,
        unroll=unroll,
        _split_transpose=_split_transpose,
    )

    ys, updates = _move_axis(
        lambda ax, leaf: jnp.moveaxis(leaf, 0, ax),
        (sliced_out_axes, sliced_in_axes),
        (ys, updates),
    )

    extract.apply_variable_updates(x_args, updates)
    extract.apply_variable_updates(broadcasts, final_broadcasts)
    carry = extract.update_carry_variables(carry, carry_out)

    if graph:
      ys = extract.from_tree2(ys)
      carry = extract.from_tree2(carry)

    if carry_arg_index is not None:
      if out_is_tuple:
        out = extract.insert_at(ys, carry_out_index, carry)
      else:
        out = carry
    else:
      out = ys

    return out

  return simple_scan_wrapper

