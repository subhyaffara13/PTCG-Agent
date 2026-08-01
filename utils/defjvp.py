
def defjvp(primitive, *jvprules):
  assert isinstance(primitive, Primitive)
  assert not primitive.multiple_results
  primitive_jvps[primitive] = partial(standard_jvp, jvprules, primitive)

