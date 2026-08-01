
def _ensure_annotate_decorated():
    """
    Lazily apply dont_skip_tracing decorator to DebugMode._annotate, to avoid circular import/initialization issues.
    """
    global _annotate_decorated
    if not _annotate_decorated:
        DebugMode._annotate = torch._dynamo.dont_skip_tracing(DebugMode._annotate)  # type: ignore[has-type]

        # Mark annotate as side-effectful so aot_eager doesn't DCE it.
        from torch.fx.node import _side_effectful_functions

        _side_effectful_functions.add(torch.ops.debug_mode_ops.annotate.default)

        # Register no-op lowering for inductor backend
        from torch._inductor.lowering import register_lowering

        @register_lowering(torch.ops.debug_mode_ops.annotate)
        def _annotate_lowering(tag: str) -> None:
            warning_once(log, 'DebugMode._annotate() is a no-op for backend="inductor"')
            return None

        _annotate_decorated = True

