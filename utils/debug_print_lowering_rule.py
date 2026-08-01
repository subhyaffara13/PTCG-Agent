
def debug_print_lowering_rule(
    ctx,
    *dyn_args,
    fmt,
    ordered,
    partitioned,
    in_tree,
    static_args,
    np_printoptions,
    has_placeholders,
    logging_record,
):
  callback = partial(
      _format_print_callback,
      fmt,
      dict(np_printoptions),
      has_placeholders,
      logging_record,
  )
  callback = _make_flat_callback(in_tree, callback, static_args)
  effect = ordered_debug_effect if ordered else debug_effect
  return debug_callback_lowering(
      ctx, *dyn_args, effect=effect, partitioned=partitioned, callback=callback
  )


def debug_print_lowering_rule(
    ctx: LoweringRuleContext,
    *args: ir.Value,
    fmt: str,
    ordered,
    partitioned,
    in_tree,
    static_args,
    np_printoptions,
    has_placeholders,
    logging_record,
):
  del partitioned, np_printoptions
  if ordered:
    raise NotImplementedError("Ordered debug_print is not supported on Pallas.")
  if has_placeholders:
    raise ValueError(
        "pl.debug_print() does not support placeholders when lowering to Triton"
    )
  args, kwargs = debugging.merge_callback_args(in_tree, args, static_args)
  if kwargs:
    raise ValueError(
        "Only positional arguments are supported by debug_print on Pallas."
    )

  tt_dialect.print_(
      f" {fmt} ",
      hex=False,
      args=args,
      is_signed=ir.DenseI32ArrayAttr.get([
          jnp.issubdtype(aval.dtype, jnp.signedinteger) for aval in ctx.avals_in
      ]),
  )
  return ()

