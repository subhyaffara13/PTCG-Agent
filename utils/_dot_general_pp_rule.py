
def _dot_general_pp_rule(eqn, context, settings) -> pp.Doc:
  # * suppress printing precision or preferred_element_type when None.
  # * print dimension_numbers as list-of-lists to be shorter.
  printed_params = {k: v for k, v in eqn.params.items() if v is not None}
  (lhs_cont, rhs_cont), (lhs_batch, rhs_batch) = eqn.params['dimension_numbers']
  printed_params['dimension_numbers'] = (
      (list(lhs_cont), list(rhs_cont)), (list(lhs_batch), list(rhs_batch)))
  printed_params.pop('out_sharding', None)  # implied by the let binder type
  return core._pp_eqn(eqn.replace(params=printed_params), context, settings)

