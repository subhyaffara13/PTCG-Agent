
def _get_state_dict(model, cpu_offload=False, half=False):
    if not cpu_offload:
        model = model.to(DEVICE_TYPE)
    if half:
        model.half()

    return model.state_dict()

