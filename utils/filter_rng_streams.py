
def filter_rng_streams(row: CallInfo):
  return not issubclass(row.type, nnx.RngStream)

