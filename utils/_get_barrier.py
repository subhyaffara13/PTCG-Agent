import math


def _get_barrier(
    aval: ShapedAbstractValue, arrival_multiplier: int
) -> mgpu.Barrier:
  assert isinstance(aval.dtype, gpu_core.BarrierType)
  num_arrivals = aval.dtype.num_arrivals
  num_barriers = math.prod(aval.shape)
  if not (orders_tc := aval.dtype.orders_tensor_core):
    num_arrivals *= arrival_multiplier
  return mgpu.Barrier(num_arrivals, num_barriers, orders_tc)

