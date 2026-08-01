
def maybe_disable_inference_mode_for_fake_prop() -> Generator[None, None, None]:
    """
    Turns off tracking of inference_mode for fake tensor propagation. With this
    context manager, when a real tensor is converted to fake tensor, the fake
    tensor looses its inference-ness.
    """
    if config.fake_tensor_disable_inference_mode:
        with torch._subclasses.meta_utils.disable_inference_mode_for_fake_prop():
            yield
    else:
        yield

