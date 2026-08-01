
def get_max_seg_per_batch(q_offsets):
  return q_offsets.shape[1] - 1 if len(q_offsets.shape) == 2 else 1

