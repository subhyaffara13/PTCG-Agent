
def _disjoint_dims(dims1, dims2, op_name, name1, name2):
  if not set(dims1).isdisjoint(set(dims2)):
    raise TypeError(f"{name1} and {name2} in {op_name} op must be disjoint; "
                    f"got: {dims1} and {dims2}.")

