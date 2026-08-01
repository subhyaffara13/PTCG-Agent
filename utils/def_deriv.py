
def def_deriv(prim, deriv):
  """
  Define the jet rule for a primitive in terms of its first derivative.
  """
  jet_rules[prim] = partial(deriv_prop, prim, deriv)

