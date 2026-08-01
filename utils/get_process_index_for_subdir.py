
def get_process_index_for_subdir(
    use_ocdbt: bool,
    override_ocdbt_process_id: Optional[str] = None,
) -> Optional[Union[int, str]]:
  """If OCDBT + merge feature is in use, returns a process index."""
  if use_ocdbt:
    return override_ocdbt_process_id or multihost.process_index()
  else:
    return None

