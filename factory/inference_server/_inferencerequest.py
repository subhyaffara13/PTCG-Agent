from . import threading

class _InferenceRequest:
    """A single inference request with a future-like result."""
    __slots__ = ["state_data", "result_event", "logits", "value"]

    def __init__(self, state_data: dict):
        self.state_data = state_data
        self.result_event = threading.Event()
        self.logits = None
        self.value = None

