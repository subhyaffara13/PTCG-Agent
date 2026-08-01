
def str_to_sdy_sharding_rule(rule: str, *,
                             reduction_factors: tuple[str, ...] = (),
                             need_replication_factors: tuple[str, ...] = (),
                             permutation_factors: tuple[str, ...] = (),
                             **factor_sizes: int) -> SdyShardingRule:
  """Constructs a SdyShardingRule object from the Einsum notation like string.

  This is done by verifying that the input Einsum notation like string and
  with optional special factors and factor sizes represents a valid sharding
  rule and converting it to an internal representation.

  Args:
    rule: The Einsum notation like string for an operation.
    reduction_factors: A tuple of factors that are reduction factors.
    need_replication_factors: A tuple of factors that are need_replication factors.
    permutation_factors: A tuple of factors that are permutation factors.
    **factor_sizes: The optional factor sizes.

  Raises:
    ValueError: If there is any problem with the rule or factor_sizes.
  """
  if not isinstance(rule, str):
    raise TypeError(f"rule must be a str, but got {type(rule)}")
  if not all(isinstance(size, int) for size in factor_sizes.values()):
    raise TypeError(
        f"factor_sizes must be a dict of str to int, but got {factor_sizes}")

  # Replace ... with a single char to simplify parsing.
  if BATCHING in rule:
    raise ValueError(f"Unknown character '{BATCHING}'")
  if "." in rule:
    rule = rule.replace("...", BATCHING)
    if "." in rule:
      raise ValueError("Character '.' must be used inside ellipsis '...'")

  try:
    operands, results = rule.split("->")
  except ValueError as e:
    raise ValueError(f"There is no -> in rule: '{rule}'") from e

  operand_mappings = _parse_values(operands)
  result_mappings = _parse_values(results)
  return SdyShardingRule(operand_mappings, result_mappings,
                         reduction_factors=reduction_factors,
                         need_replication_factors=need_replication_factors,
                         permutation_factors=permutation_factors,
                         **factor_sizes)

