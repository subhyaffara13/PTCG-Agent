
def maybe_disable_inference_mode() -> Generator[None, None, None]:
    """
    Disables torch.inference_mode for the compilation (still on at runtime).
    This simplifies the compile stack where we can assume that inference_mode
    will always be off.

    Since inference_mode is equivalent to no_grad + some optimizations (version
    counts etc), we turn on no_grad here. The other optimizations are not
    relevant to torch.compile.
    """
    is_inference_mode_on = (
        config.fake_tensor_disable_inference_mode and torch.is_inference_mode_enabled()
    )
    if is_inference_mode_on:
        with (
            torch.inference_mode(False),
            torch.no_grad(),
        ):
            yield
    else:
        yield

