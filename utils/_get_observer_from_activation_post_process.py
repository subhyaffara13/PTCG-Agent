
def _get_observer_from_activation_post_process(
    activation_post_process: ObserverBase | FakeQuantizeBase,
) -> ObserverBase:
    """
    If `activation_post_process` is an observer, return the observer.
    If `activation_post_process` is a fake quantize, return the internal observer.
    """
    if isinstance(activation_post_process, ObserverBase):
        return activation_post_process
    else:
        if not isinstance(activation_post_process, FakeQuantizeBase):
            raise AssertionError(
                "activation_post_process must be an ObserverBase or FakeQuantizeBase"
            )
        return activation_post_process.activation_post_process  # type: ignore[return-value]

