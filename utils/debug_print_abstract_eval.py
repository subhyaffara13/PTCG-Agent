
def debug_print_abstract_eval(*avals: Any, fmt: str, ordered, **kwargs):
  del avals, fmt, kwargs  # Unused.
  effect = ordered_debug_effect if ordered else debug_effect
  return [], {effect}

