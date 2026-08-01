
def emit_structseq_call(
    overloads: Sequence[PythonSignatureNativeFunctionPair],
) -> tuple[list[str], dict[str, str]]:
    """
    Generate block of named tuple type def inits, and add typeref snippets
    to declarations that use them
    """
    typenames: dict[
        str, str
    ] = {}  # map from unique name + field name lists to typedef name
    typedefs: list[str] = []  # typedef declarations and init code

    for overload in overloads:
        fieldnames = structseq_fieldnames(overload.function.func.returns)
        if not fieldnames:
            continue

        name = cpp.name(overload.function.func)  # use @with_native_function?
        tn_key = gen_structseq_typename_key(overload.function)
        typename = typenames.get(tn_key)
        if typename is None:
            typename = f"NamedTuple{'' if not typedefs else len(typedefs)}"
            typenames[tn_key] = typename
            typedefs.append(
                f"""\
static PyTypeObject* {typename} = generated::get_{name}_structseq();"""
            )

    return typedefs, typenames

