
def defbroadcasting(prim):
  fancy_primitive_batchers[prim] = partial(broadcast_batcher, prim)

