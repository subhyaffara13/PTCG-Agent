
def dma_start(operands_: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DmaStartOp:
  return DmaStartOp(operands_=operands_, loc=loc, ip=ip)


def dma_start(
    token,
    device_id,
    src_local_core_id,
    src_memory_space,
    src_id,
    src_transforms,
    dst_memory_space,
    dst_id,
    dst_transforms,
    dst_sem_id,
    src_sem_id,
    dst_device_id,
    source_info=None,
):
  shared_memory = _get_shared_memory()
  device_id = int(device_id)
  src_local_core_id = int(src_local_core_id)
  src_global_core_id = shared_memory.get_global_core_id(
      device_id, src_local_core_id
  )
  src_memory_space, src_id = int(src_memory_space), int(src_id)
  src_transforms = jax.tree.map(int, src_transforms)
  dst_memory_space, dst_id = int(dst_memory_space), int(dst_id)
  dst_transforms = jax.tree.map(int, dst_transforms)
  dst_sem_id = int(dst_sem_id)
  src_sem_id = int(src_sem_id) if src_sem_id is not None else None
  if dst_device_id is not None:
    dst_device_id = int(dst_device_id)
  else:
    dst_device_id = device_id
  dst_global_core_id = shared_memory.get_global_core_id(
      dst_device_id, src_local_core_id  # Same core on destination device as on source.
  )

  (src_sem, dst_sem), clock = shared_memory.get_semaphores_and_increment_clock(
      (src_sem_id, dst_sem_id), src_global_core_id
  )
  assert dst_sem is not None

  assert dma_id_counter is not None
  id = dma_id_counter.get_next()

  dma = DMA(
      id,
      device_id,
      src_local_core_id,
      src_memory_space,
      src_id,
      src_transforms,
      dst_device_id,
      src_local_core_id,  # Same core on destination device as on source.
      dst_memory_space,
      dst_id,
      dst_transforms,
      src_sem,
      dst_sem,
      virtual_device_id = shared_memory.get_random_virtual_device_id(),
      clock=clock,  # pyrefly: ignore[bad-argument-type]
      source_info=source_info,
  )

  if shared_memory.dma_execution_mode == 'on_wait':
    if src_sem_id is None:
      shared_memory.append_semaphore_task(
          dst_sem_id, dst_global_core_id, dma.execute_read_and_write
      )
    else:
      shared_memory.append_semaphore_task(
          src_sem_id, src_global_core_id, dma.execute_read
      )
      shared_memory.append_semaphore_task(
          dst_sem_id,
          dst_global_core_id,
          # This task for the waiting semaphore with ID `dst_sem_id` may be
          # executed before the corresponding DMA task for the sending semaphore
          # that does the DMA read. We therefore have to append a read-and-write
          # task here, instead of just a write task. If the reading for the DMA
          # has already been executed, the DMA's state will indicate this and
          # the read-write-task appended here will do the write only.
          # (Alternatively, we could have the DMA write task wait on the
          # `send_semphore`. This issue with this approach is that we do not
          # know the number of bytes transferred that `send_semaphore` should be
          # waiting for until after the reader task is done.)
          dma.execute_read_and_write,
      )
    return token

  assert shared_memory.dma_execution_mode == 'eager'
  dma.execute_read_and_write()
  return token

