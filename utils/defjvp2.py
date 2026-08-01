
def defjvp2(primitive, *jvprules):
  assert isinstance(primitive, Primitive)
  assert not primitive.multiple_results
  primitive_jvps[primitive] = partial(standard_jvp2, jvprules, primitive)

