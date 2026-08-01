
def _verbose_printer(verbose: bool | None) -> Callable[..., None]:
    """Prints messages based on `verbose`."""
    if verbose is False:
        return lambda *_, **__: None

    return lambda *args, **kwargs: print("[torch.onnx]", *args, **kwargs)


def _verbose_printer(verbose: bool | None) -> Callable[..., None]:
    """Prints messages based on `verbose`."""
    if verbose is False:
        return lambda *_, **__: None

    return lambda *args, **kwargs: print("[torch.onnx]", *args, **kwargs)

