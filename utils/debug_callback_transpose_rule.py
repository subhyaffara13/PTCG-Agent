from typing import Any, Callable

def debug_callback_transpose_rule(_, *flat_args, callback: Callable[..., Any],
                                  effect: DebugEffect, partitioned):
  del callback, effect, partitioned
  return [None for _ in flat_args]

