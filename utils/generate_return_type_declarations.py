
def generate_return_type_declarations(
    overloads: Sequence[PythonSignatureNativeFunctionPair],
) -> list[str]:
    """
    Generate block of function declarations in `python_return_types.h` to initialize
    and return named tuple for a native function.
    """
    typenames: dict[
        str, str
    ] = {}  # map from unique name + field name lists to typedef name
    declarations: list[str] = []  # function declaration to register the typedef

    for overload in overloads:
        fieldnames = structseq_fieldnames(overload.function.func.returns)
        if not fieldnames:
            continue

        name = cpp.name(overload.function.func)  # use @with_native_function?
        tn_key = gen_structseq_typename_key(overload.function)
        typename = typenames.get(tn_key)

        if typename is None:
            typename = (
                f"{name}NamedTuple{'' if not declarations else len(declarations)}"
            )
            typenames[tn_key] = typename
            declarations.append(f"PyTypeObject* get_{name}_structseq();")

    return declarations

