
def is_tensorboard_available():
    return importlib.util.find_spec("tensorboard") is not None or importlib.util.find_spec("tensorboardX") is not None


def is_tensorboard_available() -> bool:
    return is_package_available("tensorboard")

