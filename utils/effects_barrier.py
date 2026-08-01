
def effects_barrier():
  """Waits until existing functions have completed any side-effects."""
  dispatch.runtime_tokens.block_until_ready()

