
def install_importhook(config: Config) -> rewrite.AssertionRewritingHook:
    """Try to install the rewrite hook, raise SystemError if it fails."""
    config.stash[assertstate_key] = AssertionState(config, "rewrite")
    config.stash[assertstate_key].hook = hook = rewrite.AssertionRewritingHook(config)
    sys.meta_path.insert(0, hook)
    config.stash[assertstate_key].trace("installed rewrite import hook")

    def undo() -> None:
        hook = config.stash[assertstate_key].hook
        if hook is not None and hook in sys.meta_path:
            sys.meta_path.remove(hook)

    config.add_cleanup(undo)
    return hook

