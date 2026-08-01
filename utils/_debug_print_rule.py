
def _debug_print_rule(
    ctx: LoweringRuleContext,
    *dyn_args,
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
  args, kwargs = debugging.merge_callback_args(in_tree, dyn_args, static_args)
  if kwargs:
    raise ValueError(
        "Only positional arguments are supported by debug_print on Pallas."
    )

  is_scalar_inputs = [not aval.shape for aval in ctx.avals_in]
  is_all_scalars = all(is_scalar_inputs)
  is_single_vector = len(is_scalar_inputs) == 1 and not is_scalar_inputs[0]
  if not (is_all_scalars or is_single_vector):
    raise ValueError(
        "All inputs to debug_print must be all scalars or a single vector, but"
        f" got {ctx.avals_in}"
    )

  # Scalar case.
  if is_all_scalars:
    if has_placeholders:
      primitives.check_debug_print_format(fmt, *args)
      if not all(
          isinstance(arg.type, ir.IntegerType) and arg.type.width == 32
          for arg in args
      ):
        raise TypeError(
            "All arguments must be 32-bit integers when using"
            " placeholders (`{...}`). If you need to print values of other types,"
            " remove placeholders from the format string."
        )

      # TPU expects $0, $1 etc as placeholders.
      fmt = "".join(
          f"{text}${spec}{idx}" if field is not None else text
          for idx, (text, field, spec, _) in enumerate(
              string.Formatter().parse(fmt)
          )
      )

    tpu.log(args, fmt, formatted=has_placeholders)
    return ()

  # Vector case.
  # Copy the array to vmem for logging.
  # Note that the shape of the array must be explicitly provided here. This is
  # because the underlying implementation aligns shapes to tile boundaries,
  # potentially altering the original shape and making it unrecoverable.
  if len(ctx.avals_in) != 1:
    raise ValueError(
        "Only one vector input to debug_print is supported."
    )
  (aval,) = ctx.avals_in
  (arg,) = args

  if not has_placeholders or not fmt.endswith("{}"):
    raise ValueError("For vector input, the format string must end with {}.")

  fmt = fmt[:-2]

  region = tpu.RegionOp(())
  with ir.InsertionPoint(region.body):
    element_type = _dtype_to_ir_type(aval.dtype)
    ref_type = ir.MemRefType.get(
        aval.shape,
        element_type,
        memory_space=ir.Attribute.parse("#tpu.memory_space<vmem>"),
    )
    ref = memref.alloca(ref_type, [], [])

    index_type = ir.IndexType.get()
    zero = arith.constant(index_type, 0)
    indices = [zero] * len(aval.shape)
    vector.store(arg, ref, indices)
    tpu.log_buffer(ref, aval.shape, fmt)
    tpu.yield_([])
  return ()

