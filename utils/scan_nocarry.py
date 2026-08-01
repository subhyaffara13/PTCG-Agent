
def scan_nocarry(f: Callable[[Carry, X], tuple[Carry, Y]],
         xs: X | None = None,
         length: int | None = None,
         reverse: bool = False,
         unroll: int | bool = 1) -> tuple[Carry, Y]:
  dbg_body = api_util.debug_info("scan", f, (xs,), {})
  xs_flat = FlatTree.flatten(xs)
  check_no_transformed_refs_args(lambda: dbg_body, list(xs_flat))
  del xs
  xs_avals = xs_flat.map(core.typeof)
  length = _infer_scan_length(list(xs_flat), list(xs_avals), length)

  # TODO(dougalm): handle disable_jit
  if config.mutable_array_checks.value:
    check_no_aliased_ref_args(lambda: dbg_body, list(xs_avals), list(xs_flat))

  x_avals = xs_avals.map(lambda aval: core.mapped_leading_aval(length, aval))
  # TODO(dougalm): promote away all weak types
  args_avals = FlatTree.pack(((x_avals,), {}))
  jaxpr, y_avals = pe.trace_to_jaxpr(f, args_avals, dbg_body)
  jaxpr, consts = pe.separate_consts(jaxpr)

  if config.mutable_array_checks.value:
    _check_no_aliased_closed_over_refs(dbg_body, consts, list(xs_flat))

  disallowed_effects = effects.control_flow_allowed_effects.filter_not_in(jaxpr.effects)
  if disallowed_effects:
    raise NotImplementedError(
        f'Effects not supported in `scan`: {disallowed_effects}')

  unroll = core.concrete_or_error(
      None, unroll,
      "The `unroll` argument to `scan` expects a concrete `int` or `bool` "
      "value.")
  if isinstance(unroll, bool):
    unroll = max(length, 1) if unroll else 1
  if unroll < 0:
    raise ValueError("`unroll` must be a `bool` or a non-negative `int`.")

  args = list(consts) + list(xs_flat)
  # TODO(dougalm): handle traceable-level forwarding
  out = Scan3(
      extensives = [False] * len(consts) + [True] * len(xs_flat),
      length=length, jaxpr=jaxpr, reverse=reverse, unroll=unroll)(args)

  return y_avals.update(out).unflatten()

