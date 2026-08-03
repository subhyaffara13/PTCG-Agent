import sys

def script_method(fn):
    if sys.version_info >= (3, 14):
        warnings.warn(
            "`torch.jit.script_method` is not supported in Python 3.14+ and may break. "
            "Please switch to `torch.compile` or `torch.export`.",
            DeprecationWarning,
        )
    else:
        warnings.warn(
            "`torch.jit.script_method` is deprecated. Please switch to `torch.compile` or `torch.export`.",
            DeprecationWarning,
        )
    if not _enabled:
        return fn
    # NOTE: we need to traverse two frames here because the meta-class frame
    # for ScriptModule will be present, as opposed to invoking @script on a
    # a function or invoking define() on a CompilationUnit.
    # The stack will look like:
    #
    # 0. createResolutionCallback()
    # 1. script_method()
    # 2. ScriptModule metaclass frame
    # 3. Surrounding scope
    #
    # createResolutionCallback internally adds 1 to get us to the scope of this
    # function (the calling function). Adding 2 gets us to the proper surrounding scope.
    _rcb = _jit_internal.createResolutionCallbackFromFrame(frames_up=2)
    ast = get_jit_def(fn, fn.__name__, self_name="ScriptModule")
    return ScriptMethodStub(_rcb, ast, fn)

