
def subtests(request: SubRequest) -> Subtests:
    """Provides subtests functionality."""
    capmam = request.node.config.pluginmanager.get_plugin("capturemanager")
    suspend_capture_ctx = (
        capmam.global_and_fixture_disabled if capmam is not None else nullcontext
    )
    return Subtests(request.node.ihook, suspend_capture_ctx, request, _ispytest=True)

