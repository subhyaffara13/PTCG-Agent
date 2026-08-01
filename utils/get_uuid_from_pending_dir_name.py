
def get_uuid_from_pending_dir_name(pending_dir_name: str) -> str:
  return pending_dir_name.split("_")[-1]

