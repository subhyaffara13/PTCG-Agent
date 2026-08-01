
def is_probably_a_function(runtime: Any) -> bool:
    return (
        isinstance(
            runtime,
            (
                types.FunctionType,
                types.BuiltinFunctionType,
                types.MethodType,
                types.BuiltinMethodType,
            ),
        )
        or (inspect.ismethoddescriptor(runtime) and callable(runtime))
        or (isinstance(runtime, types.MethodWrapperType) and callable(runtime))
    )

