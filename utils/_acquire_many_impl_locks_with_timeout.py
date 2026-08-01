
def _acquire_many_impl_locks_with_timeout(
    *impls: _CacheImpl,
    timeout: float | None = None,
) -> Generator[None, None, None]:
    with ExitStack() as stack:
        for impl in impls:
            stack.enter_context(impl.lock(timeout))
        yield

