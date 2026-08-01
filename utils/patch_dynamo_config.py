
def patch_dynamo_config(
    arg1: str | dict[str, Any] | tuple[tuple[str, Any], ...] | None = None,
    arg2: Any = None,
    **kwargs: Any,
) -> DynamoConfigPatchProxy:
    """
    A wrapper around torch._dynamo.config.patch that can be traced by Dynamo to
    temporarily change config values DURING tracing.

    See _allowed_config_patches for the list of allowed config patches.

    Arguments are the same as with torch._dynamo.config.patch.

    Can be used as a decorator or a context manager.

    User code SHOULD NOT MODIFY the return value of this function.

    WARNING: changing Dynamo config during tracing can lead to unpredictable tracing behavior!
        Proceed only as advised!
    """
    if isinstance(arg1, tuple):
        arg1 = dict(arg1)
    config_patch = torch._dynamo.config.patch(arg1, arg2, **kwargs)
    _patch_dynamo_config_check(config_patch.changes)
    # check for valid patching using config_patch.changes
    return DynamoConfigPatchProxy(config_patch)

