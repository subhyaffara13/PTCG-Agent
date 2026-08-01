
def _get_weight_observer(observer):
    # FakeQuantize observer
    if hasattr(observer, "activation_post_process"):
        observer = observer.activation_post_process
    # UniformQuantizationObserverBase observer
    return observer

