
def set_tpu_interpret_mode(params: InterpretParams = InterpretParams()):
  config.pallas_tpu_interpret_mode_context_manager.set_global(params)

