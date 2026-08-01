
def _is_random_datapipe(datapipe: DataPipe) -> bool:
    return hasattr(datapipe, "set_seed") and inspect.ismethod(datapipe.set_seed)

