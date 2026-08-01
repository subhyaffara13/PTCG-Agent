
def ensure_tuple(dimension_numbers):
  _to_tuple = lambda x: x if isinstance(x, tuple) else tuple(x)

  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  lhs_contract = _to_tuple(lhs_contract)
  rhs_contract = _to_tuple(rhs_contract)
  lhs_batch = _to_tuple(lhs_batch)
  rhs_batch = _to_tuple(rhs_batch)
  return (lhs_contract, rhs_contract), (lhs_batch, rhs_batch)

