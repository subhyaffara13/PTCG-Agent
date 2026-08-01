
def _move_to_device(model: nn.Module, move_to_device: bool):
    return model.to(DEVICE_TYPE) if move_to_device else model

