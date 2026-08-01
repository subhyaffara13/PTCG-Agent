
def _warn_teardown_exception(
    hook_name: str, hook_impl: HookImpl, e: BaseException
) -> None:
    msg = "A plugin raised an exception during an old-style hookwrapper teardown.\n"
    msg += f"Plugin: {hook_impl.plugin_name}, Hook: {hook_name}\n"
    msg += f"{type(e).__name__}: {e}\n"
    msg += "For more information see https://pluggy.readthedocs.io/en/stable/api_reference.html#pluggy.PluggyTeardownRaisedWarning"  # noqa: E501
    warnings.warn(PluggyTeardownRaisedWarning(msg), stacklevel=6)

