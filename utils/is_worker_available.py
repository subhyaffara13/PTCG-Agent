
def is_worker_available() -> bool:
    return hasattr(js, "Worker") and hasattr(js, "Blob")


def is_worker_available() -> bool:
    return hasattr(js, "Worker") and hasattr(js, "Blob")

