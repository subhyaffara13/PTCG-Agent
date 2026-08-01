
def override_cudagraphs(
    fwd: bool | None = None, bwd: bool | None = None
) -> CudagraphOverrideContextManager:
    """
    Context manager/decorator to override cudagraph recording for compiled graphs.

    When used as a context manager, overrides cudagraphs for all graph segments
    within the block (including across graph breaks).

    When used as a decorator, marks a function so that any compiled graph
    inlining it will have cudagraphs overridden.

    Args:
        fwd: If False, disable cudagraphs for forward. If True, force enable.
             If None, don't override.
        bwd: If False, disable cudagraphs for backward. If True, force enable.
             If None, don't override.
    """
    return CudagraphOverrideContextManager(fwd=fwd, bwd=bwd)

