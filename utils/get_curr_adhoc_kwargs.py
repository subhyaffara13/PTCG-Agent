
def get_curr_adhoc_kwargs() -> dict[str, Any] | None:
  if _CURR_ADHOC_KWARGS is None:
    return None
  else:
    return dict(_CURR_ADHOC_KWARGS)

