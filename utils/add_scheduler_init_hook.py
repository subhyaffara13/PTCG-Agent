
def add_scheduler_init_hook(
    pre_fn: Callable[..., Any], post_fn: Callable[..., Any] | None = None
) -> Any:
    """
    Add hook functions to be called at the beginning and end of Scheduler.__init__.
    Used for unit tests.
    """
    from torch._inductor.scheduler import Scheduler

    orig_fn = Scheduler.__init__

    def wrapper(scheduler: Any, nodes: Any) -> Any:
        pre_fn(scheduler, nodes)
        out = orig_fn(scheduler, nodes)
        if post_fn:
            post_fn(scheduler, nodes)
        return out

    return unittest.mock.patch.object(Scheduler, "__init__", wrapper)

