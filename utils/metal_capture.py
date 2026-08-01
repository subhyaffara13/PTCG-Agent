
def metal_capture(fname: str) -> Iterator[None]:
    """Context manager that enables capturing of Metal calls into gputrace"""
    try:
        torch._C._mps_startCapture(fname)  # type: ignore[attr-defined]
        yield
        # Drain all the work that were enqueued during the context call
        torch.mps.synchronize()
    finally:
        torch._C._mps_stopCapture()  # type: ignore[attr-defined]

