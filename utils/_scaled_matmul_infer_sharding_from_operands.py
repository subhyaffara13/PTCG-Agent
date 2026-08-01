
def _scaled_matmul_infer_sharding_from_operands(
    preferred_element_type, mesh, shapes, output_shape
  ):
  shardings = tree_util.tree_map(lambda x: x.sharding, shapes)
  _check_shardings(shardings)

  return _get_output_sharding(shardings)

