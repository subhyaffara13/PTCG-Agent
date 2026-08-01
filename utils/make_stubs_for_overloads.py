
def make_stubs_for_overloads(overload_info):
    overload_stubs = []
    for orig_fn, overloads in overload_info.items():
        orig_ast = get_jit_def(
            orig_fn, orig_fn.__name__, self_name="RecursiveScriptModule"
        )
        for overload_name, overload_fn in overloads:
            _check_no_signature(overload_fn)
            over_ast = get_jit_def(
                overload_fn, overload_fn.__name__, self_name="RecursiveScriptModule"
            )
            new_ast = torch._C._replace_overloaded_method_decl(
                over_ast.decl(), orig_ast, overload_name
            )
            _rcb = _jit_internal.createResolutionCallbackFromClosure(orig_fn)
            overload_stubs.append(ScriptMethodStub(_rcb, new_ast, overload_fn))
    return overload_stubs

