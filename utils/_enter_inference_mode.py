
def _enter_inference_mode(mode):
    mode_context = torch._C._InferenceMode(mode)
    mode_context.__enter__()
    return mode_context

