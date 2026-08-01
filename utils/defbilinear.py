
def defbilinear(prim, lhs_rule, rhs_rule):
  assert isinstance(prim, Primitive)
  lhs_jvp = lambda g, x, y, **kwargs: prim.bind(g, y, **kwargs)
  rhs_jvp = lambda g, x, y, **kwargs: prim.bind(x, g, **kwargs)
  defjvp(prim, lhs_jvp, rhs_jvp)
  fancy_transposes[prim] = partial(fancy_bilinear_transpose, lhs_rule, rhs_rule)
  # TODO(mattjj,yashkatariya): remove next line if downstream doesnt need it
  primitive_transposes[prim] = partial(bilinear_transpose, lhs_rule, rhs_rule)

