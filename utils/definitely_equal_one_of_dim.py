
def definitely_equal_one_of_dim(d1: DimSize, dlist: Sequence[DimSize]) -> bool:
  return any(definitely_equal(d1, d) for d in dlist)

