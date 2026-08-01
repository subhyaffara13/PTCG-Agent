
def transform_with_lock(
    builder: IRBuilder, mgr_v: Value, target: Lvalue | None, body: GenFunc, line: int
) -> None:
    """Optimized 'with' for librt.threading.Lock.

    Generate a simple try/finally with direct acquire/release calls.
    Lock.__exit__ never suppresses exceptions, so we don't need the
    full PEP 343 try/except/finally machinery.
    """
    # __enter__: acquire the lock
    value = builder.primitive_op(lock_acquire_op, [mgr_v], line)

    mgr = builder.maybe_spill(mgr_v)

    def try_body() -> None:
        if target:
            builder.assign(builder.get_assignment_target(target), value, line)
        body()

    def finally_body() -> None:
        # __exit__: release the lock (ignoring exception info)
        builder.primitive_op(lock_release_op, [builder.read(mgr, line)], line)

    transform_try_finally_stmt(builder, try_body, finally_body, line)

