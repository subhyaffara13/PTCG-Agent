
def thread_safe_generator() -> torch.Generator | None:
    """Returns a thread-safe random number generator for use in DataLoader workers.
    This function provides a convenient way for transforms and user code to use
    thread-safe random number generation without manually checking worker context.
    When called in a DataLoader thread worker, returns the worker's thread-local
    :class:`torch.Generator`. When called in the main process or process workers,
    returns ``None`` (which causes PyTorch functions to use the default global RNG).
    Returns:
        Optional[torch.Generator]: Thread-local generator in thread workers, None otherwise.
    Example::
        >>> from torch.random import thread_safe_generator
        >>> generator = thread_safe_generator()
        >>> torch.randint(0, 10, (5,), generator=generator)
    Example with transforms::
        >>> from torch.random import thread_safe_generator
        >>> class MyRandomTransform:
        ...     def __call__(self, img):
        ...         generator = thread_safe_generator()
        ...         offset = torch.randint(0, 10, (2,), generator=generator)
        ...         return img[..., offset[0]:, offset[1]:]
    """
    # Lazy import to avoid circular dependency during torch module initialization
    # torch.__init__ loads torch.random early, but torch.utils.data triggers
    # torch.distributed which needs torch to be fully initialized
    from torch.utils.data import get_worker_info

    worker_info: WorkerInfo | None = get_worker_info()
    if (
        worker_info is not None
        and worker_info.worker_method == "thread"
        and worker_info.rng is not None
    ):
        return worker_info.rng.torch_generator
    return None

