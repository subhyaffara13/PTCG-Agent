
def get_prop_to_input_output(in_shardings, out_shardings,
                             num_ordered_effects):
  allow_prop_to_inputs = (False,) * num_ordered_effects + tuple(
      isinstance(i, UnspecifiedValue) for i in in_shardings)
  allow_prop_to_outputs = (False,) * num_ordered_effects + tuple(
      isinstance(o, UnspecifiedValue) or mlir.contains_unconstrained(o)
      for o in out_shardings)
  return allow_prop_to_inputs, allow_prop_to_outputs

