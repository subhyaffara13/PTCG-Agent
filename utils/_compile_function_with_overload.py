
def _compile_function_with_overload(overload_fn, qual_name, impl_fn):
    overload_decl = get_jit_def(overload_fn, overload_fn.__name__).decl()
    overload_signature = torch.jit.annotations.get_signature(
        overload_fn, None, None, inspect.ismethod(overload_fn)
    )
    impl_ast = get_jit_def(impl_fn, impl_fn.__name__)
    overload_defaults = get_default_args(overload_fn)
    implementation_defaults = get_default_args(impl_fn)
    _rcb = _jit_internal.createResolutionCallbackFromClosure(impl_fn)
    _check_overload_defaults(
        implementation_defaults, overload_defaults, overload_decl.range()
    )
    fn = torch._C._jit_script_compile_overload(
        qual_name,
        overload_decl,
        impl_ast,
        _rcb,
        implementation_defaults,
        overload_signature,
    )
    return fn

