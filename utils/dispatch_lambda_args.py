
def dispatch_lambda_args(
    ps: PythonSignature, f: NativeFunction, symint: bool = True
) -> tuple[DispatchLambdaArgument, ...]:
    if isinstance(ps, PythonSignatureDeprecated):
        schema = ps.deprecated_schema
    else:
        schema = f.func

    # Start with cpp arguments - dispatch lambda signature always include 'self'
    cpp_args = cpp.arguments(
        arguments=schema.arguments,
        faithful=False,
        symint=symint,
        method=False,
        cpp_no_default_args=f.cpp_no_default_args,
    )
    out_args: set[str] = {a.name for a in schema.arguments.out}

    # Convert from cpp argument to lambda argument
    def dispatch_lambda_arg(cpp_arg: Binding) -> DispatchLambdaArgument:
        type_str = cpp_arg.type
        is_out_arg = cpp_arg.name in out_args
        if ps.method and cpp_arg.name == "self":
            # For method's 'self', we can use 'const Tensor &' and simply ignore mutability!
            type_str = "const at::Tensor &"
        else:
            # For other cases we need prevent dangling refs to temps (unless it's
            # unpacked scattered output)
            # The reason is explained in the comments above and in 'dispatch_lambda_return_str()'.
            # TODO: avoid this special handling?
            ensure_temp_safe = len(out_args) <= 1 or not is_out_arg
            if ensure_temp_safe:
                type_str = {
                    "at::Tensor &": "at::Tensor",
                }.get(type_str, type_str)
        return DispatchLambdaArgument(
            name=cpp_arg.name,
            type_str=type_str,
            is_out_arg=is_out_arg,
        )

    return tuple(map(dispatch_lambda_arg, cpp_args))

