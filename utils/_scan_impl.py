
def _scan_impl(*args, reverse, length, num_consts, num_carry, jaxpr,
               unroll):
  consts, carry, xs_ = split_list(args, [num_consts, num_carry])
  _, y_avals = split_list(jaxpr.out_avals, [num_carry])
  if unroll == 0:
    num_trips, remainder = 0, length
  else:
    num_trips, remainder = divmod(length, unroll)

  xs_rem: tuple[Array, ...] = ()
  if unroll != 1 and num_trips == 1 and remainder == 0:
    # In that case, we explicitly want to fully unroll the loop. Put everything
    # into the remainder block and avoid lowering to a while loop.
    num_trips, remainder = 0, length
  if unroll == 1:
    xss = xs_
    yss = _map(partial(_empty_array, (length,), (None,)), y_avals)
  else:
    if remainder:
      if not reverse:
        xs_, xs_rem = unzip2(_map(partial(_split_leading, num_trips*unroll), xs_))
      else:
        xs_rem, xs_ = unzip2(_map(partial(_split_leading, remainder), xs_))
    if num_trips:
      xss = [lax.reshape(x, (num_trips, unroll, *x.shape[1:])) for x in xs_]
      yss = _map(partial(_empty_array, (num_trips, unroll), (None, None)), y_avals)
    else:
      yss = _map(partial(_empty_array, (num_trips * unroll,), (None,)), y_avals)

  def inner(n, carry, xs):
    ys = []
    if unroll == 1:
      carry_y = eval_jaxpr_p.bind(*consts, *carry, *xs, jaxpr=jaxpr)
      return split_list(carry_y, [num_carry])
    for i_ in range(n):
      i = n - i_ - 1 if reverse else i_
      x = [slicing.index_in_dim(x, i, keepdims=False) for x in xs]
      carry_y = eval_jaxpr_p.bind(*consts, *carry, *x, jaxpr=jaxpr)
      carry, y = split_list(carry_y, [num_carry])
      ys.append(y)
    ys = list(reversed(ys)) if reverse else ys
    return carry, _map(_stack, zip(*ys))

  def body_fun(while_carry):
    i_, carry, yss = while_carry
    with use_abstract_mesh(core.typeof(i_).sharding.mesh):
      i = num_trips - i_ - 1 if reverse else i_
    xs = []
    for x in xss:
      with use_abstract_mesh(core.typeof(x).sharding.mesh):
        o = slicing.dynamic_index_in_dim(
            x, i, keepdims=False, allow_negative_indices=False)
      xs.append(o)
    carry, ys = inner(unroll, carry, xs)
    out_yss = []
    for y, upd in zip(yss, ys):
      with use_abstract_mesh(core.typeof(y).sharding.mesh):
        o = slicing.dynamic_update_index_in_dim(
            y, upd, i, 0, allow_negative_indices=False)
      out_yss.append(o)
    return i_ + 1, carry, out_yss

  def cond_fun(while_carry):
    i, _, _ = while_carry
    return i < num_trips

  if num_trips:
    i = lax._const(num_trips, 0)
    _, carry, yss = while_loop(cond_fun, body_fun, (i, carry, yss))
  if unroll != 1 and num_trips != 0:
    ys = [lax.reshape(ys, (num_trips * unroll, *ys.shape[2:])) for ys in yss]
  else:
    ys = yss
  if remainder:
    carry, ys_rem = inner(remainder, carry, xs_rem)
    ys = _map(_concat, ys, ys_rem) if not reverse else _map(_concat, ys_rem, ys)
  # If any carry leaf is unreduced, we need to add a reshard to
  # typeof(carry).sharding which inserts a sharding_constraint so that shardy
  # knows not to AR at the boundary of while. This is a no-op at the trace level
  # but during lowering time, it inserts an extra sharding constraint.
  carry = tree_map(_constrain_unreduced, carry)
  ys = tree_map(_constrain_unreduced, ys)
  return [*carry, *ys]

