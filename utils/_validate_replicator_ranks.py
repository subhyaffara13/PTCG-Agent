
def _validate_replicator_ranks(
    *, num_nodes: int, node_rank: int, peer_ranks: List[int]
) -> None:
  """Validates the rank fields written to `replicator.yaml`."""
  if num_nodes <= 0:
    raise ValueError(f'num_nodes must be positive, got {num_nodes}.')
  if not 0 <= node_rank < num_nodes:
    raise ValueError(
        f'Invalid node_rank={node_rank} for num_nodes={num_nodes}.'
    )
  invalid_peer_ranks = [
      rank for rank in peer_ranks if not 0 <= rank < num_nodes
  ]
  if invalid_peer_ranks:
    raise ValueError(
        f'Invalid peer_ranks={invalid_peer_ranks} for num_nodes={num_nodes}.'
    )
  if node_rank in peer_ranks:
    raise ValueError(
        f'peer_ranks must not include node_rank={node_rank}: {peer_ranks}.'
    )
  if len(peer_ranks) != len(set(peer_ranks)):
    raise ValueError(f'peer_ranks must be unique, got {peer_ranks}.')

