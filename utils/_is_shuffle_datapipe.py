
def _is_shuffle_datapipe(datapipe: DataPipe) -> bool:
    return (
        hasattr(datapipe, "set_shuffle")
        and hasattr(datapipe, "set_seed")
        and inspect.ismethod(datapipe.set_shuffle)
        and inspect.ismethod(datapipe.set_seed)
    )

