
def generate_return_type_definition_and_registrations(
    overloads: Sequence[PythonSignatureNativeFunctionPair],
) -> tuple[list[str], list[str]]:
    """
    Generate block of function in `python_return_types.cpp` to initialize
    and return named tuple for a native function which returns named tuple
    and registration invocations in same file.
    """
    typenames: dict[
        str, str
    ] = {}  # map from unique name + field name lists to typedef name
    definitions: list[str] = []  # function definition to register the typedef
    registrations: list[str] = []  # register call for the typedef

    for overload in overloads:
        fieldnames = structseq_fieldnames(overload.function.func.returns)
        if not fieldnames:
            continue

        fields = ", ".join(f'{{"{fn}", ""}}' for fn in fieldnames)

        name = cpp.name(overload.function.func)  # use @with_native_function?
        tn_key = gen_structseq_typename_key(overload.function)
        typename = typenames.get(tn_key)

        if typename is None:
            typename = f"{name}NamedTuple{'' if not definitions else len(definitions)}"
            typenames[tn_key] = typename
            definitions.append(
                f"""\
PyTypeObject* get_{name}_structseq() {{
    static PyStructSequence_Field NamedTuple_fields[] = {{ {fields},  {{nullptr}} }};
    static PyTypeObject {typename};
    static bool is_initialized = false;
    static PyStructSequence_Desc desc = {{ "torch.return_types.{name}", nullptr, NamedTuple_fields, {len(fieldnames)} }};
    if (!is_initialized) {{
        PyStructSequence_InitType(&{typename}, &desc);
        {typename}.tp_repr = (reprfunc)torch::utils::returned_structseq_repr;
        is_initialized = true;
    }}
    return &{typename};
}}
"""
            )
            registrations.append(
                f'addReturnType(return_types_module, "{name}", generated::get_{name}_structseq());'
            )

    return definitions, registrations

