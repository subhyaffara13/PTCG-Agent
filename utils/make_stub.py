
def make_stub(func, name):
    rcb = _jit_internal.createResolutionCallbackFromClosure(func)
    ast = get_jit_def(func, name, self_name="RecursiveScriptModule")
    return ScriptMethodStub(rcb, ast, func)

