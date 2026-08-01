
def is_ray_available():
    return importlib.util.find_spec("ray") is not None

