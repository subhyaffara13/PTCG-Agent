
def def_comp(prim, comp, **kwargs):
  """
  Define the jet rule for a primitive in terms of a composition of simpler primitives.
  """
  jet_rules[prim] = partial(jet2, comp, **kwargs)

