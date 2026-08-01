
def node_id() -> int:
  return int(os.environ.get("JOB_COMPLETION_INDEX", "0"))

