
def _set_max_registers_abstract_eval(n, *, action):
  del n, action  # Unused.
  return (), {gpu_core._memory_effect}

