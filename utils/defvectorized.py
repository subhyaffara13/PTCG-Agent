
def defvectorized(prim):
  fancy_primitive_batchers[prim] = partial(vectorized_batcher, prim)

