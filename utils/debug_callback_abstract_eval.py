from typing import Any, Callable

def debug_callback_abstract_eval(*flat_avals, callback: Callable[..., Any],
                                 effect: DebugEffect, partitioned: bool):
  del flat_avals, callback, partitioned
  return [], {effect}

