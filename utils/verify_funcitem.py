
def verify_funcitem(
    stub: nodes.FuncItem, runtime: MaybeMissing[Any], object_path: list[str]
) -> Iterator[Error]:
    if isinstance(runtime, Missing):
        yield Error(object_path, "is not present at runtime", stub, runtime)
        return

    if not is_probably_a_function(runtime):
        yield Error(object_path, "is not a function", stub, runtime)
        if not callable(runtime):
            return

    # Look the object up statically, to avoid binding by the descriptor protocol
    static_runtime = _static_lookup_runtime(object_path)

    if isinstance(stub, nodes.FuncDef):
        for error_text in _verify_abstract_status(stub, runtime):
            yield Error(object_path, error_text, stub, runtime)
        for error_text in _verify_final_method(stub, runtime, static_runtime):
            yield Error(object_path, error_text, stub, runtime)

    for message in _verify_static_class_methods(stub, runtime, static_runtime, object_path):
        yield Error(object_path, "is inconsistent, " + message, stub, runtime)

    signature = safe_inspect_signature(runtime)
    runtime_is_coroutine = inspect.iscoroutinefunction(runtime)

    if signature:
        stub_sig = Signature.from_funcitem(stub)
        runtime_sig = Signature.from_inspect_signature(signature)
        runtime_sig_desc = describe_runtime_callable(signature, is_async=runtime_is_coroutine)
        stub_desc = str(stub_sig)
    else:
        runtime_sig_desc, stub_desc = None, None

    # Don't raise an error if the stub is a coroutine, but the runtime isn't.
    # That results in false positives.
    # See https://github.com/python/typeshed/issues/7344
    if runtime_is_coroutine and not stub.is_coroutine:
        yield Error(
            object_path,
            'is an "async def" function at runtime, but not in the stub',
            stub,
            runtime,
            stub_desc=stub_desc,
            runtime_desc=runtime_sig_desc,
        )

    if not signature:
        return

    for message in _verify_signature(
        stub_sig,
        runtime_sig,
        function_name=stub.name,
        warn_runtime_is_object_init=runtime is object.__init__,
    ):
        yield Error(
            object_path,
            "is inconsistent, " + message,
            stub,
            runtime,
            runtime_desc=runtime_sig_desc,
        )

