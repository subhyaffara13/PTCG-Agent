
def sdy_sharding_rule_to_mlir(
  rule: SdyShardingRule,
  operand_types: list[ir.Type],
  result_types: list[ir.Type],) -> ir.Attribute:
  """Builds the MLIR representation for the sharding rule.

  This is done by verifying that the rule is consistent with the types of
  the operation and converting the Einsum notation like string to
  OpShardingRuleAttr.
  """
  if len(rule.operand_mappings) != len(operand_types):
    raise ValueError(
      f"Sharding rule has {len(rule.operand_mappings)} operands, but the operation"
      f" has {len(operand_types)} operands")
  if len(rule.result_mappings) != len(result_types):
    raise ValueError(
      f"Sharding rule has {len(rule.result_mappings)} results, but the operation"
      f" has {len(result_types)} results")
  if not all(isinstance(t, ir.Type) for t in operand_types + result_types):
    raise TypeError(
        f"operand_types and result_types must be a list of ir.Type, but got"
        f" {operand_types} and {result_types}")

  factors_to_indices_sizes: OrderedDict[str, list[int]] = OrderedDict()
  types = operand_types + result_types
  UNKNOWN = -1  # Representation for unknown factor size or factor index.

  def get_message_for_value(i):
    if i >= len(operand_types):
      return f"{i - len(operand_types)}th result"
    else:
      return f"{i}th operand"

  def get_rank_for_value(i):
    return ir.ShapedType(types[i]).rank

  def get_size_for_value_dim(i, j):
    return ir.ShapedType(types[i]).shape[j]

  def add_factor(factor, size):
    """Adds a factor to factors_to_indices_sizes.

    `size` may be a dimensions size, a user specified factor size, or UNKNOWN
    if a factor is first used as in a compound factor and then used for a
    whole dimension. If a factor is not for a leading batching dimension and
    it corresponds to multiple sizes, the smallest size is used.
    """
    factor_index, factor_size = factors_to_indices_sizes.get(factor, [UNKNOWN, UNKNOWN])
    if factor_index != UNKNOWN:
      # Not the first time seeing the factor.
      if size != UNKNOWN and factor_size != UNKNOWN and factor_size != size:
        if _BATCHING_DIM_FACTOR_PREFIX in factor:
          raise ValueError(f"Batching dimension {factor[1:]} corresponds to "
                           f"two sizes: {factor_size} and {size}")
        else:
          if size < factor_size:
            # Use the smaller size to update the factor size.
            factor_size = UNKNOWN
      if size != UNKNOWN and factor_size == UNKNOWN:
        factors_to_indices_sizes[factor] = [factor_index, size]
    else:
      # First time seeing the factor.
      factor_index = len(factors_to_indices_sizes)
      factors_to_indices_sizes[factor] = [factor_index, size]

  def add_batching_dim_factor(batch_grp, batch_dim_order, factor_size):
    add_factor(_get_batching_dim_factor_name(batch_grp, batch_dim_order), factor_size)

  def build_dim_mapping_for_compound_factors(i, j, factors):
    accumulated_size = 1
    all_indices = []
    for factor in factors:
      factor_index, factor_size = factors_to_indices_sizes[factor]
      accumulated_size *= factor_size
      all_indices.append(factor_index)

    dim_size = get_size_for_value_dim(i, j)
    if accumulated_size != dim_size:
      raise ValueError(
          f"{get_message_for_value(i)} actual size {dim_size} doesn't match"
          f" the size {accumulated_size} derived from the compound factors"
          f" {factors}")

    return sdy.DimMappingAttr.get(factor_indices=all_indices)

  def factors_to_indices(factors):
    return [factors_to_indices_sizes[factor][0] for factor in factors]

  # Add factors and their sizes in the order they appear in the rule,
  # including the batching dimensions represented by ellipsis.
  batching_group_to_rank: dict[str, int] = {}
  for i, mapping in enumerate(rule.operand_mappings + rule.result_mappings):
    value = tuple(mapping)
    if value and _is_batching(value[0]):
      batching_group = _get_batching_group(value[0])
      value = value[1:]
    else:
      batching_group = None
    rule_rank = len(value)
    op_rank = get_rank_for_value(i)
    # The number of dimensions represented by ellipsis.
    current_batching_rank = 0
    if batching_group is not None and op_rank >= rule_rank:
      current_batching_rank = op_rank - rule_rank
    if batching_group is not None:
      ellipsis_rank = batching_group_to_rank.get(batching_group, None)
      if ellipsis_rank is None:
        ellipsis_rank = current_batching_rank
        batching_group_to_rank[batching_group] = ellipsis_rank
      elif ellipsis_rank != current_batching_rank:
        raise ValueError(
          "Ellipsis represents different number of leading dimensions"
          f" {ellipsis_rank} and {current_batching_rank}")
    rule_rank += current_batching_rank
    if rule_rank != op_rank:
      msg = get_message_for_value(i)
      raise ValueError(
        f"Sharding rule {msg} has rank {rule_rank}, but the operation"
        f" {msg} has rank {op_rank}")

    for j in range(current_batching_rank):
      add_batching_dim_factor(batching_group, j, get_size_for_value_dim(i, j))

    for j, dim in enumerate(value):
      if isinstance(dim, str):
        add_factor(dim, get_size_for_value_dim(i, j + current_batching_rank))
      else:
        for factor in dim:
          add_factor(factor, rule.factor_sizes.get(factor, UNKNOWN))

  # Build the tensor mappings for each operand and result.
  tensor_mappings = []
  for i, mapping in enumerate(rule.operand_mappings + rule.result_mappings):
    value = tuple(mapping)
    dim_mappings = []
    if value and _is_batching(value[0]):
      batching_group = _get_batching_group(value[0])
      value = value[1:]
      if batching_group in batching_group_to_rank:
        current_batching_rank = batching_group_to_rank[batching_group]
      else:
        raise ValueError("Unreachabled code")
    else:
      current_batching_rank = 0
      batching_group = None

    for j in range(current_batching_rank):
      assert batching_group is not None
      dim_mappings.append(
        sdy.DimMappingAttr.get(factor_indices=[
          factors_to_indices_sizes[_get_batching_dim_factor_name(batching_group, j)][0]]))

    for j, dim in enumerate(value):
      if isinstance(dim, str):
        dim_mappings.append(
          sdy.DimMappingAttr.get(
            factor_indices=[factors_to_indices_sizes[dim][0]]))
      else:
        dim_mappings.append(
          build_dim_mapping_for_compound_factors(
            i, j + current_batching_rank, dim))

    tensor_mappings.append(
      sdy.TensorMappingAttr.get(dim_mappings=dim_mappings))

  return sdy.OpShardingRuleAttr.get(
      factor_sizes=[item[1] for item in factors_to_indices_sizes.values()],
      operand_mappings=tensor_mappings[0:len(operand_types)],
      result_mappings=tensor_mappings[len(operand_types):],
      is_custom=True,
      reduction_factors=factors_to_indices(rule.reduction_factors),
      need_replication_factors=factors_to_indices(rule.need_replication_factors),
      permutation_factors=factors_to_indices(rule.permutation_factors),
      )

