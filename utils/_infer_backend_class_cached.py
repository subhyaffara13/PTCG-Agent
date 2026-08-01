
def _infer_backend_class_cached(cls: type) -> str:
    return cls.__module__.split(".")[0]

