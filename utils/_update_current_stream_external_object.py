
def _update_current_stream_external_object() -> Generator[None, None, None]:
    """Update the external object registry so custom ops see the capture stream.

    During cudagraph recording/warmup the current stream differs from the
    trace-time default stream.  The external object at CURRENT_STREAM_INDEX
    must reflect the actual current stream so that custom ops (e.g. event
    record/wait) executed during capture use the right stream.
    """
    set_external_object_by_index(CURRENT_STREAM_INDEX, torch.cuda.current_stream())
    yield

