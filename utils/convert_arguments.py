
def convert_arguments(f: NativeFunction) -> tuple[list[Binding], list[str]]:
    # we need the 'self' argument so method needs to be False
    args = (
        CppSignatureGroup.from_native_function(f, method=False)
        .most_faithful_signature()
        .arguments()
    )
    code_list = [
        f"c10::IValue {args[i].name} = std::move(peek(stack, {i}, {len(args)}));"
        for i in range(len(args))
    ] + [""]
    binding_list = []
    for arg in args:
        # expecting only Argument
        if not isinstance(arg.argument, Argument):
            raise Exception(  # noqa: TRY002
                f"Unexpected argument type, expecting `Argument` but got {arg}"
            )
        argument: Argument = arg.argument
        unboxed_name, _, code, decl = argumenttype_ivalue_convert(
            argument.type,
            argument.name,
            mutable=argument.is_write,
        )
        code_list.extend(decl)
        code_list.extend(code)
        binding_list.append(arg.with_name(unboxed_name))
    return binding_list, code_list

