
def get_shm_size_in_mb():
  """Get /dev/shm size in MB.

  Returns:
    Size in MB if /dev/shm exists, None if it doesn't exist, 0 on error.
  """
  try:
    shm_path = "/dev/shm"
    if not os.path.exists(shm_path):
      return 0

    stat = os.statvfs(shm_path)
    # Total size in bytes
    shm_size_bytes = stat.f_blocks * stat.f_frsize
    shm_size_mb = shm_size_bytes / (1024 * 1024)

    return shm_size_mb

  except Exception as e:  # pylint: disable=broad-exception-caught
    logger.debug("Failed to check /dev/shm size: %s", e)
    return 0

