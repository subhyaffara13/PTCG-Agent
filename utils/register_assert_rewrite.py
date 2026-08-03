import sys

def register_assert_rewrite(*names: str) -> None:
    """Register one or more module names to be rewritten on import.

    This function will make sure that this module or all modules inside
    the package will get their assert statements rewritten.
    Thus you should make sure to call this before the module is
    actually imported, usually in your __init__.py if you are a plugin
    using a package.

    :param names: The module names to register.
    """
    for name in names:
        if not isinstance(name, str):
            msg = "expected module names as *args, got {0} instead"  # type: ignore[unreachable]
            raise TypeError(msg.format(repr(names)))
    rewrite_hook: RewriteHook
    for hook in sys.meta_path:
        if isinstance(hook, rewrite.AssertionRewritingHook):
            rewrite_hook = hook
            break
    else:
        rewrite_hook = DummyRewriteHook()
    rewrite_hook.mark_rewrite(*names)

