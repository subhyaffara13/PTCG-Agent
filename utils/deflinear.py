
def deflinear(prim):
  jet_rules[prim] = partial(linear_prop, prim)


def deflinear(primitive, transpose_rule):
  primitive_jvps[primitive] = partial(linear_jvp, primitive)
  primitive_transposes[primitive] = partial(linear_transpose, transpose_rule)

