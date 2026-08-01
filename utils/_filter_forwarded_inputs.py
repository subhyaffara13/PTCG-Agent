
def _filter_forwarded_inputs(outs, ins):
  idxs: dict[int, int] = {id(x): i for i, x in enumerate(ins)}
  return [o for o in outs if id(o) not in idxs], [idxs.get(id(o)) for o in outs]

