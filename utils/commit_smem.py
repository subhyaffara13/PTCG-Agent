
def commit_smem():
  """Commits all reads from/writes to SMEM, making them visible to TMA and MMA operations."""
  commit_smem_p.bind()

