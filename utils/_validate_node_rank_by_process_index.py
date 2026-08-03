from typing import List

def _validate_node_rank_by_process_index(
    node_rank_by_process_index: List[int], *, num_nodes: int
) -> None:
  """Validates a ProcessIndex -> NodeRank mapping."""
  if len(node_rank_by_process_index) != num_nodes:
    raise ValueError(
        'ProcessIndex->NodeRank mapping must have one entry per node, got '
        f'{node_rank_by_process_index} for num_nodes={num_nodes}.'
    )
  invalid_entries = [
      (process_index, node_rank)
      for process_index, node_rank in enumerate(node_rank_by_process_index)
      if not 0 <= node_rank < num_nodes
  ]
  if invalid_entries:
    raise ValueError(
        'ProcessIndex->NodeRank mapping contains invalid entries for '
        f'num_nodes={num_nodes}: {invalid_entries}.'
    )
  if len(set(node_rank_by_process_index)) != num_nodes:
    raise ValueError(
        'ProcessIndex->NodeRank mapping must be one-to-one, got '
        f'{node_rank_by_process_index}.'
    )

