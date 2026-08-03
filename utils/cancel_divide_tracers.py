import math


def cancel_divide_tracers(num, denom):
  partition = lambda l: partition_list([isinstance(d, Tracer) for d in l], l)
  num, num_tracers = partition(num)
  denom, denom_tracers = partition(denom)
  if num_tracers or denom_tracers:
    factor = _cancel_divide(num_tracers, denom_tracers)
    if factor is not None:
      size1 = math.prod(num)
      size2 = math.prod(denom)
      if size1 == size2 or size2 != 0:
        return factor * (size1 // size2 if size1 != size2 else 1)

