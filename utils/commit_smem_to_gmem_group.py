
def commit_smem_to_gmem_group() -> None:
  """Commits all issued but uncommitted SMEM->GMEM copies to a group."""
  commit_group_p.bind()

