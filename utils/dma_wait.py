
def dma_wait(tag_mem_ref: _ods_ir.Value[_ods_ir.MemRefType], tag_indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], num_elements: _ods_ir.Value[_ods_ir.IndexType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DmaWaitOp:
  return DmaWaitOp(tagMemRef=tag_mem_ref, tagIndices=tag_indices, numElements=num_elements, loc=loc, ip=ip)


def dma_wait(token, device_id, local_core_id, sem_id, size, source_info=None):
  shared_memory = _get_shared_memory()

  device_id = int(device_id)
  local_core_id = int(local_core_id)
  sem_id = int(sem_id)
  size = int(size)

  global_core_id = shared_memory.get_global_core_id(device_id, local_core_id)

  (sem,), _ = shared_memory.get_semaphores_and_increment_clock(
      [sem_id], global_core_id
  )
  assert sem is not None
  sem.wait(
      size,
      global_core_id,
      has_tasks=True,
      logging_info=interpret_utils.TPULoggingInfo(
          device_id=device_id, local_core_id=local_core_id,
          source_info=source_info,
      ),
  )
  return token

