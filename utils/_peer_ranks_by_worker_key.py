
def _peer_ranks_by_worker_key(
    workers: Sequence[Worker],
) -> tuple[tuple[int, ...], ...]:
  """Returns peer ranks by matching Pathways workers across slices by task."""
  ranks_by_task_and_slice = {worker.key: worker.rank for worker in workers}
  slices = sorted({worker.key[1] for worker in workers})
  peers = []
  for worker in workers:
    task_index, slice_index = worker.key
    peers.append(
        tuple(
            ranks_by_task_and_slice[(task_index, peer_slice)]
            for peer_slice in slices
            if peer_slice != slice_index
        )
    )
  return tuple(peers)

