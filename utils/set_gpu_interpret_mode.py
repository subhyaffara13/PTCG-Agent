
def set_gpu_interpret_mode(params: InterpretGPUParams = InterpretGPUParams()):
  config.pallas_tpu_interpret_mode_context_manager.set_global(params)

