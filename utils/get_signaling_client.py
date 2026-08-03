import logging

def get_signaling_client() -> SignalingClient:
  """Returns the signaling client to use for the current environment."""
  if multihost.is_jax_distributed_client_initialized():
    logging.info("Using JaxDistributedSignalingClient")
    return JaxDistributedSignalingClient()

  # Verify that we are either in a Pathways backend, Pathways colocated
  # runtime, or single process environment.
  if (
      multihost.is_pathways_backend()
      or multihost.is_pathways_colocated_runtime_active()
      or (process_count := multihost.process_count()) == 1
  ):
    logging.info("Using ThreadSafeKeyValueSignalingClient")
    return ThreadSafeKeyValueSignalingClient()

  raise RuntimeError(
      "ThreadSafeKeyValueSignalingClient should only be used in a single"
      f" controller setup, process count: {process_count}."
  )


def get_signaling_client() -> SignalingClient:
  return _SignalingClient(signaling_client.get_signaling_client())

