
def transfer_guard(new_val: str) -> Generator[None, None, None]:
  """A contextmanager to control the transfer guard level for all transfers.

  For more information, see
  https://docs.jax.dev/en/latest/transfer_guard.html

  Args:
    new_val: The new thread-local transfer guard level for all transfers.

  Yields:
    None.
  """
  with contextlib.ExitStack() as stack:
    stack.enter_context(transfer_guard_host_to_device(new_val))
    stack.enter_context(transfer_guard_device_to_device(new_val))
    stack.enter_context(transfer_guard_device_to_host(new_val))
    stack.enter_context(_transfer_guard(new_val))
    yield

