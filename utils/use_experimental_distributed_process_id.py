import logging

def use_experimental_distributed_process_id() -> bool:
  """Returns True if the experimental distributed process id is enabled."""
  try:
    return EXPERIMENTAL_ORBAX_USE_DISTRIBUTED_PROCESS_ID.value
  except Exception:  # pylint: disable=broad-exception-caught
    logging.log_first_n(
        logging.INFO,
        '[thread=%s] Failed to get flag value for'
        ' EXPERIMENTAL_ORBAX_USE_DISTRIBUTED_PROCESS_ID.',
        1,
        threading.current_thread().name,
    )
    return False

