
def dce_sink(val, *, prevent_mlir_dce: bool = False):
  sink = partial(dce_sink_p.bind, prevent_mlir_dce=prevent_mlir_dce)
  tree_util.tree_map(sink, val)

