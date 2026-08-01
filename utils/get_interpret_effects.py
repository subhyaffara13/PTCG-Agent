
def get_interpret_effects(interpret: Any) -> Set[effects.Effect]:
  if (mosaic_tpu_interpret is not None
      and isinstance(interpret, mosaic_tpu_interpret.InterpretParams)):
    return mosaic_tpu_interpret.get_interpret_effects()
  if (mosaic_gpu_interpret is not None
      and isinstance(interpret, mosaic_gpu_interpret.InterpretGPUParams)):
    return mosaic_gpu_interpret.get_interpret_effects()
  return effects.no_effects


def get_interpret_effects() -> set[effects.Effect]:
  return {callback._OrderedIOEffect}


def get_interpret_effects():
  return {callback._OrderedIOEffect, callback._IOEffect}

