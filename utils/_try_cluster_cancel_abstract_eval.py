
def _try_cluster_cancel_abstract_eval(*args, **params):
  del args, params

  return (), {gpu_core._memory_effect}

