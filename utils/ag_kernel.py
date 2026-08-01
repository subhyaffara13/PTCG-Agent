
def ag_kernel(x_ref, o_ref, send_sem, recv_sem, *, axis_name: str,
              mesh: jax.sharding.Mesh):
  my_id = lax.axis_index(axis_name)
  # TODO(sharadmv): could speed this up having the first remote DMA go from
  # x_ref->o_ref immediately instead of a blocking HBM copy.
  with jax.named_scope("initial_copy"):
    pltpu.async_copy(x_ref, o_ref.at[my_id], recv_sem[0]).wait()

  with jax.named_scope("neighbour_lookup"):
    axis_size = lax.axis_size(axis_name)
    left_neighbor = get_neighbor(my_id, mesh, axis_name, direction="left")
    right_neighbor = get_neighbor(my_id, mesh, axis_name, direction="right")

  with jax.named_scope("main_barrier"):
    sem = pltpu.get_barrier_semaphore()
    pl.semaphore_signal(sem, 1, device_id=left_neighbor)
    pl.semaphore_signal(sem, 1, device_id=right_neighbor)
    pl.semaphore_wait(sem, 2)

  shard_size = x_ref.shape[0]
  right_dma, left_dma = None, None
  # Main strategy for this AG: carve up our input into two slices. Send
  # each slice along each direction until they reach every device.
  for i in range(axis_size - 1):
    right_slot = my_id - i
    right_slice = pl.ds(shard_size // 2, shard_size // 2)
    slot = jnp.where(right_slot < 0, axis_size + right_slot, right_slot)
    if right_dma:
      with jax.named_scope("wait_right_dma"):
        right_dma.wait()
    right_dma = pltpu.async_remote_copy(
        o_ref.at[slot, right_slice],
        o_ref.at[slot, right_slice],
        send_sem[1],
        recv_sem[1],
        device_id=right_neighbor,
    )

    left_slot = my_id + i
    left_slice = pl.ds(0, shard_size // 2)
    slot = lax.rem(left_slot, axis_size)
    if left_dma:
      with jax.named_scope("wait_left_dma"):
        left_dma.wait()
    left_dma = pltpu.async_remote_copy(
        o_ref.at[slot, left_slice],
        o_ref.at[slot, left_slice],
        send_sem[0],
        recv_sem[0],
        device_id=left_neighbor,
    )
  with jax.named_scope("wait_all_dma"):
    assert right_dma is not None
    assert left_dma is not None
    right_dma.wait()
    left_dma.wait()

