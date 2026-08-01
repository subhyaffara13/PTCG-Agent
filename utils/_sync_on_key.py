
def _sync_on_key(key: str | None, extra_tag: str = "") -> None:
  if key is None:
    return
  full_key = f"{key}-{extra_tag}" if extra_tag else key
  if (client := distributed.global_state.client) is not None:
    client.wait_at_barrier(full_key, timeout_in_ms=_TIMEOUT_SEC * 1000)

