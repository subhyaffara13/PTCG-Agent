
def _smem_tree_size(smem_buffers: ShapeTree) -> int:
  leaves = jax.tree.leaves(
      smem_buffers, is_leaf=lambda x: isinstance(x, Union)
  )
  size = 0
  for l in leaves:
    match l:
      case Union(members):
        size += max(_smem_tree_size(s) for s in members)
      case (
          TMABarrier(num_barriers)
          | ClusterBarrier(num_barriers=num_barriers)
          | Barrier(num_barriers=num_barriers)
      ):
        if size % utils.MBARRIER_BYTES:
          raise NotImplementedError(
              "Misaligned barrier allocation. Expected smem size"
              f" ({size} bytes) to be divisible by the size of the barrier:"
              f" {utils.MBARRIER_BYTES} bytes."
          )
        size += num_barriers * utils.MBARRIER_BYTES
      case TMEM(_):
        # TODO(justinfu): This can trigger misaligned barrier allocations
        # if TMEM is requested before barriers b/c it's not divisible by 8.
        size += 4  # i32 takes up 4 bytes
      case _:
        size += _count_buffer_bytes(l)
  return size

