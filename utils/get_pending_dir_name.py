
def get_pending_dir_name(source_name: str) -> str:
  return (
      f"{source_name}{PENDING_DIR_SUFFIX}_{time.time_ns()}_{uuid.uuid4().hex}"
  )

