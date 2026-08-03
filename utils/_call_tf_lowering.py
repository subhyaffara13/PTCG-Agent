import logging

def _call_tf_lowering(
    ctx: mlir.LoweringRuleContext,
    *args_op,
    platform,
    function_flat_tf,
    args_flat_sig_tf,
    has_side_effects,
    ordered,
    call_tf_graph,
    output_avals,
    **_,
):
  # We use the same TF lowering device as for the embedding JAX computation.
  # One example when this is needed is when the code refers to variables on one
  # device. Or, for sharding annotations (only supported on TPU).

  if platform in ["cpu", "tpu"]:
    tf_platform = platform.upper()
  elif platform == "cuda":
    tf_platform = "GPU"
  else:
    raise ValueError("platform {platform} not supported")

  concrete_function_flat_tf = _get_concrete_function_tf(function_flat_tf, args_flat_sig_tf)

  captured_inputs = []
  if concrete_function_flat_tf.captured_inputs:
    # The function uses either captured variables or tensors.
    msg = (
        "call_tf works best with a TensorFlow function that does not capture "
        "variables or tensors from the context. "
        "See https://github.com/jax-ml/jax/blob/main/jax/experimental/jax2tf/README.md#limitations-of-call_tf for a discussion. "
        f"The following captures were found {concrete_function_flat_tf.captured_inputs}")
    logging.warning(msg)
    for inp in concrete_function_flat_tf.captured_inputs:
      if inp.dtype == tf.resource:  # A variable; lookup by handle
        inp_vars = [v for v in concrete_function_flat_tf.variables if inp is v.handle]
        assert len(inp_vars) == 1, f"Found {inp_vars}"
        captured_inputs.append(inp_vars[0])
      else:
        captured_inputs.append(inp)

  # The following use case happens when we call_tf a restored saved model that
  # includes parameters (hence functions closing over tf.Variable), and then
  # we jax2tf.convert it with native serialization, under tf.function (or
  # for saving to saved model). The `np.asarray(inp)` fails because it thinks
  # it is in TF graph mode. The `tf.init_scope()` lifts out of function-building
  # graph scopes, and allows us to read the values of the variables
  with tf.init_scope():
    captured_ops, _ = mlir.ir_tree_registry.flatten([
        mlir.ir_constant(np.asarray(inp)) for inp in captured_inputs
    ])
    captured_ops = tuple(captured_ops)

  if call_tf_graph:
    with jax2tf_internal.inside_call_tf():
      return emit_tf_embedded_graph_custom_call(
          ctx,
          concrete_function_flat_tf,
          tuple(args_op) + captured_ops,
          has_side_effects,
          ordered,
          output_avals,
      )

  def convert_to_spec(x):
    if isinstance(x, tf.TensorSpec):
      return x
    else:
      return tf.TensorSpec.from_tensor(x)

  args_tf_flat = [convert_to_spec(a) for a in args_flat_sig_tf]

  with jax2tf_internal.inside_call_tf():
    try:
      func_tf_hlo = function_flat_tf.experimental_get_compiler_ir(
          *args_tf_flat
      )(stage="hlo_serialized", platform_name=tf_platform)
    except Exception as e:
      msg = ("Error compiling TensorFlow function (see below for the caught exception)." +
             "\ncall_tf can used " +
              "in a staged context (under jax.jit, lax.scan, etc.) only with " +
              "compilable functions with static output shapes.\n" +
              "See https://github.com/jax-ml/jax/blob/main/jax/experimental/jax2tf/README.md#limitations-of-call_tf for a discussion." +
             "\n\nCaught TensorFlow exception: " + str(e))
      raise ValueError(msg) from e

  stablehlo = _jax.mlir.hlo_to_stablehlo(func_tf_hlo)
  submodule = ir.Module.parse(stablehlo)
  symtab = ir.SymbolTable(submodule.operation)
  main = cast(func_dialect.FuncOp, symtab["main"])
  callee_result_types = main.type.results
  fn = mlir.merge_mlir_modules(ctx.module_context.module,
                               f"call_tf_{function_flat_tf.name}",
                               submodule,
                               dst_symtab=ctx.module_context.symbol_table)
  call = func_dialect.CallOp(callee_result_types,
                             ir.FlatSymbolRefAttr.get(fn),
                             [*args_op, *captured_ops])
  flat_results = call.results

  if ordered:
    raise NotImplementedError(
        "ordered=True is not supported in the jitted context without"
        " `call_tf_graph=True`"
    )

  outputs = []
  for op, res_type in zip(flat_results, callee_result_types):
    if not res_type.has_static_shape:
      msg = (
          "Compiled TensorFlow function has dynamic output shape "
          + f"{res_type}. call_tf can used in a staged context (under jax.jit,"
          " lax.scan, etc.) only with compilable functions with static"
          " output shapes. See"
          " https://github.com/jax-ml/jax/blob/main/jax/experimental/jax2tf/README.md#limitations-of-call_tf"
          " for a discussion."
      )
      raise ValueError(msg)

    res_dtype = _mlir_type_to_numpy_dtype(res_type.element_type)
    # Canonicalize the results; e.g., makes them x32 if JAX is in 32-bit mode
    jax_res_dtype = dtypes.canonicalize_dtype(res_dtype)
    if res_dtype != jax_res_dtype:
      op = hlo.ConvertOp(
          mlir.aval_to_ir_type(ctx.module_context, core.ShapedArray(res_type.shape, jax_res_dtype)),
          op,
      ).result
    outputs.append(op)
  return outputs

