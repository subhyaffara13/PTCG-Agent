from typing import Callable

def register_once(
    event_name: str,
    callback: Callable[..., None],
    info: Hashable,
) -> None:
  """Register the IPython event once (replace the previous event if exists).

  Alias for `InteractiveShell.events.register` but replaces previous event
  if it exists.

  This avoids duplicated events after ecolab reload or running cell twice.

  Args:
    event_name: Forwarded to `ip.events.register`
    callback: Forwarded to `ip.events.register`
    info: If an event with the same info already exists, it is replaced.
  """
  ip = IPython.get_ipython()

  # Even if hash is non-deterministic, we only need to check registration within
  # the same run.
  info = hash(info)

  # Remove the previous callback (if any)
  for old_callback in ip.events.callbacks[event_name]:
    if getattr(old_callback, '__ecolab_event__', None) == info:
      ip.events.unregister(event_name, old_callback)
      break

  # Mark the function (so it can be cleared when reloaded)
  callback.__ecolab_event__ = info

  ip.events.register(event_name, callback)

