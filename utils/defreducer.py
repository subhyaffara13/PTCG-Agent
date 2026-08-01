
def defreducer(prim):
  fancy_primitive_batchers[prim] = partial(reducer_batcher, prim)

