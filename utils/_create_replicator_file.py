import logging
import os
from typing import List

def _create_replicator_file(
    file_path: epath.Path,
    *,
    run_name: str,
    num_nodes: int,
    data_parallelism: int,
    node_rank: int,
    peer_ranks: List[int],
    backup_interval_minutes: int,
):
  """Creates a replicator file."""
  _validate_replicator_ranks(
      num_nodes=num_nodes, node_rank=node_rank, peer_ranks=peer_ranks
  )
  temp_file = epath.Path(file_path) / _TEMP_REPLICATOR_FILE_NAME
  replicator_file = epath.Path(file_path) / _REPLICATOR_FILE
  replicator_yaml = f"""job-name: {run_name}
  framework: orbax
  assume-data-parallelism: {data_parallelism}
  node-rank: {node_rank}
  nodes: {num_nodes}
  peer-ranks: {peer_ranks}
  backup-interval-minutes: {backup_interval_minutes}"""
  final_yaml = '\n'.join(
      line.strip() for line in replicator_yaml.split('\n')
  )
  logging.info(
      f'Writing replicator file to {replicator_file} (via temp {temp_file})'
  )
  logging.vlog(1, 'Replicator YAML contents:\n%s', final_yaml)
  temp_file.write_text(final_yaml)
  os.replace(temp_file, replicator_file)
  logging.info('Replicator file written and renamed successfully.')

