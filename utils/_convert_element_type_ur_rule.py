
def _convert_element_type_ur_rule(operand, *, new_dtype, weak_type, sharding):
  unreduced = (sharding.spec.unreduced
               if sharding is not None and isinstance(sharding, NamedSharding)
               and sharding.spec.unreduced else getu(operand))
  reduced = (sharding.spec.reduced
             if sharding is not None and isinstance(sharding, NamedSharding)
             and sharding.spec.reduced else getr(operand))
  return unreduced, reduced

