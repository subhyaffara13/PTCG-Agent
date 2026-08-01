
def _build_sdy_sharding_rule(module_context, num_batch_dims, avals_in, avals_out):
  letters = iter(string.ascii_letters)
  lhs = ", ".join(
      _sdy_rule_for_aval(letters, num_batch_dims, a) for a in avals_in)
  rhs = ", ".join(
      _sdy_rule_for_aval(letters, num_batch_dims, a) for a in avals_out)
  sdy_sharding_rule = str_to_sdy_sharding_rule(f"{lhs} -> {rhs}")
  flat_in_types, _ = mlir.ir_tree_registry.flatten([mlir.aval_to_ir_types(module_context, a) for a in avals_in])
  flat_out_types, _ = mlir.ir_tree_registry.flatten([mlir.aval_to_ir_types(module_context, a) for a in avals_out])
  return sdy_sharding_rule_to_mlir(
      sdy_sharding_rule,
      flat_in_types,
      flat_out_types)

