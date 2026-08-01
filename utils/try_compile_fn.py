
def try_compile_fn(fn, loc):
    if _jit_internal.is_ignored_fn(fn):
        # Don't do anything for @ignore'd functions
        return None

    if isinstance(fn, torch.nn.Module):
        # Since modules are callable pybind recognizes them as functions, but
        # don't do anything for them
        return None

    if not inspect.isfunction(fn) and not inspect.ismethod(fn):
        raise RuntimeError(
            f"`{fn}` is not a function. Recursive scripting only supports "
            "Python functions or methods currently.\n"
            f"Consider manually annotating `{fn}` with @torch.jit.script."
        )

    # The object returned by __prepare_scriptable__ might have a different closure.
    # Resolve it here to get the right resolution callback.
    fn = fn.__prepare_scriptable__() if hasattr(fn, "__prepare_scriptable__") else fn  # type: ignore[operator]

    # We don't have the actual scope where the function was defined, but we can
    # extract the necessary info from the closed over variables on the function
    # object
    rcb = _jit_internal.createResolutionCallbackFromClosure(fn)
    return torch.jit.script(fn, _rcb=rcb)

