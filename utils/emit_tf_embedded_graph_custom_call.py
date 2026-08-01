
def emit_tf_embedded_graph_custom_call(
    ctx: mlir.LoweringRuleContext,
    concrete_function_flat_tf,
    operands: Sequence[ir.Value],
    has_side_effects,
    ordered,
    output_avals,
):
  """Emits a custom call referencing a tf.Graph embedding of the TF function.

  All call_tf called function information is stored in tf.metadata.
  This includes:
  (1) The called function name: This name will be used by the runtime to execute
  the callback.
  (2) The called function index in the XLACallModule `function_list` attribute.
  """
  call_tf_concrete_function_list = jax2tf_internal.get_thread_local_state_call_tf_concrete_function_list()
  if call_tf_concrete_function_list is None:
    raise ValueError(
        "call_tf_graph=True only support exporting by jax2tf.convert currently."
    )
  # TODO(necula): It is dangerous to modify global state when lowering because
  # there are a number of lowering caches that only cache the StableHLO.
  # See call_tf_test.py:test_multi_platform_call_tf_graph.
  called_index = add_to_call_tf_concrete_function_list(
      concrete_function_flat_tf, call_tf_concrete_function_list)
  tf_backend_config = {
      "has_token_input_output": ir.BoolAttr.get(ordered),
      "called_index": mlir.i64_attr(called_index),
  }
  result_avals = ctx.avals_out if ctx.avals_out is not None else ()

  operands = list(operands)
  flat_res_types, _ = mlir.ir_tree_registry.flatten([mlir.aval_to_ir_type(ctx.module_context, aval) for aval in result_avals])
  result_types = list(flat_res_types)
  if ordered:
    operands.insert(0, ctx.tokens_in.get(call_tf_ordered_effect))
    result_types.insert(0, mlir.token_type())

  custom_call = hlo.CustomCallOp(
      result_types,
      operands,
      call_target_name=ir.StringAttr.get("tf.call_tf_function"),
      has_side_effect=ir.BoolAttr.get(has_side_effects),
      api_version=mlir.i32_attr(2),
      called_computations=ir.ArrayAttr.get([]),
      backend_config=ir.StringAttr.get(""),
  )
  # Store TF metadata in unregistered attribute
  custom_call.attributes["tf.backend_config"] = ir.DictAttr.get(
      tf_backend_config
  )

  results = list(custom_call.results)
  if ordered:
    token = results.pop(0)
    ctx.set_tokens_out(ctx.tokens_in.update_tokens(
        mlir.TokenSet({call_tf_ordered_effect: token})))

  return results

