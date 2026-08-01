
def mark_stream(stream: torch.cuda.Stream, annotation: str | dict[str, Any]):
    """Switch to stream, inject its ID into annotation, and mark kernels.

    If *stream* is already the current stream, no stream switch or stream ID
    injection happens — the kernels stay on whatever stream is active (which
    keeps the trace faithful when e.g. FSDP uses the current stream for
    copy-in instead of a separate one).
    """
    if not _annotations_enabled:
        with torch.cuda.stream(stream):
            yield
        return
    if stream.cuda_stream == torch.cuda.current_stream().cuda_stream:
        with mark_kernels(annotation):
            yield
    else:
        if isinstance(annotation, str):
            annotation = {"str": annotation}
        if isinstance(annotation, dict):
            annotation["stream"] = _get_stream_id(stream)
        with torch.cuda.stream(stream):
            with mark_kernels(annotation):
                yield

