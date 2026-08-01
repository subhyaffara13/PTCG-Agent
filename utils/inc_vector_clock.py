
def inc_vector_clock(x: VectorClock, global_core_id: int):
  if global_core_id >= len(x):
    raise ValueError(f'device_id={global_core_id} is out of range for x={x}')
  assert global_core_id < len(x)
  x[global_core_id] += 1

