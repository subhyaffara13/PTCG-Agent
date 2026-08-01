
def wait_smem_to_gmem(n: int, wait_read_only: bool = False) -> None:
  """Waits until no more than the most recent ``n`` SMEM->GMEM copies issued by the calling thread are in flight.

  Args:
    n: The maximum number of copies in flight to wait for.
    wait_read_only: If ``True``, wait for the in flight copies to finish
      reading from SMEM. The writes to GMEM are not waited for.
  """
  wait_smem_to_gmem_p.bind(n, wait_read_only=wait_read_only)

