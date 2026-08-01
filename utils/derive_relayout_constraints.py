
def derive_relayout_constraints(
    value_sites_for_variable: ValueSitesForVariable,
) -> list[cs.Relayout]:
  """Derives relayout constraints from the given variable mapping."""
  constraints: list[cs.Relayout] = []
  variable_for_value_site: dict[ValueSite, cs.Variable] = {}
  for variable, value_sites in value_sites_for_variable.items():
    for value_site in value_sites:
      if value_site in variable_for_value_site:
        raise ValueError(
            f"{value_site} is mapped to both {variable} and "
            f"{variable_for_value_site[value_site]}"
        )
    variable_for_value_site |= {k: variable for k in value_sites}

  visited: set[cs.Variable] = set()
  for variable, value_sites in value_sites_for_variable.items():
    for value_site in value_sites:
      # We can only relayout variables that are in registers.
      if value_site.memory_space != cs.MemorySpace.REG:
        continue

      elt_bitwidth = utils.bitwidth(value_site.value.type.element_type)
      if value_site.type == VariableType.OPERAND:
        pr = producer_result(value_site)
        producer_variable = variable_for_value_site[pr]
        # Only add the constraint if we haven't already created that constraint
        # when processing this variable as one of the producer's consumers.
        if producer_variable not in visited:
          # The producer of a variable must be relayout-able to the variable.
          constraints.append(
              cs.Relayout(
                  producer_variable, variable, elt_bitwidth, strict=True
              )
          )
      elif value_site.type in (VariableType.RESULT, VariableType.ARGUMENT):
        for co in consumer_operands(value_site):
          consumer_variable = variable_for_value_site[co]
          # Only add the constraint if we haven't already created that
          # constraint when processing this variable as the consumer's producer.
          if consumer_variable not in visited:
            # A variable must be relayout-able to its consumers.
            constraints.append(
                cs.Relayout(
                    variable, consumer_variable, elt_bitwidth, strict=True
                )
            )
    visited.add(variable)
  return constraints

