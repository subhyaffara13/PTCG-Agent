
def _debug_print_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    fmt: str,
    ordered,
    partitioned,
    in_tree,
    static_args,
    np_printoptions,
    has_placeholders,
    logging_record,
):
  del partitioned, np_printoptions, in_tree, static_args
  def fail(reason: str) -> NoReturn:
    raise NotImplementedError(
        f"pl.debug_print() {reason} when lowering to SparseCore"
    )

  if ordered:
    fail("does not support ordered print")
  if has_placeholders:
    fail("does not support placeholders")

  match args:
    case []:
      tpu.log(inputs=[], tag=fmt)
    case [arg] if isinstance(arg.type, ir.MemRefType):
      tpu.log_buffer(arg, ctx.avals_in[0].shape, fmt)
    case [arg]:
      tpu.log(inputs=[arg], tag=fmt)
    case _:
      fail("does not support multiple inputs")
  return []


def _debug_print_lowering_rule(
    ctx: LoweringRuleContext,
    *args,
    fmt,
    ordered,
    partitioned,
    in_tree,
    static_args,
    np_printoptions,
    has_placeholders,
    logging_record,
):
  del partitioned, np_printoptions, has_placeholders
  if ordered:
    raise NotImplementedError("Ordered debug_print is not supported on Pallas.")
  args, kwargs = debugging.merge_callback_args(in_tree, args, static_args)
  if kwargs:
    raise ValueError(
        "Only positional arguments are supported by debug_print on Pallas."
    )
  primitives.check_debug_print_format(fmt, *args)
  if not any(aval.shape for aval in ctx.avals_in):
    scope = mgpu.ThreadSubset.WARPGROUP
    if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
      scope = mgpu.ThreadSubset.WARP
    mgpu.debug_print(
        fmt,
        *(
            _ensure_ir_value(arg, aval.dtype)
            for arg, aval in zip(args, ctx.avals_in)
        ),
        scope=scope
    )
  elif len(ctx.avals_in) == 1:
    if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
      raise NotImplementedError("Can only print scalars in warp-level code.")
    [arg] = args
    if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
      mgpu.dialect.debug_print(fmt, arg)
    else:
      arg.debug_print(fmt)

  else:
    raise NotImplementedError(
        "debug_print only supports printing of scalar values, or a single array"
        " value when using the Mosaic GPU backend."
    )

  return ()

