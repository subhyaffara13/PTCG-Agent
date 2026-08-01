
def transform_code_object(
    code: types.CodeType,
    transformations: Callable[
        [list[Instruction], dict[str, Any]], Optional["DynamoTracerOutput"]
    ],
    safe: bool = False,
) -> tuple[types.CodeType, Optional["DynamoTracerOutput"]]:
    keys = get_code_keys()
    code_options = {k: getattr(code, k) for k in keys}
    assert len(code_options["co_varnames"]) == code_options["co_nlocals"]

    instructions = cleaned_instructions(code, safe)
    # propagate line nums again for added instructions
    propagate_line_nums(instructions)

    tracer_output = transformations(instructions, code_options)
    _, bytecode = clean_and_assemble_instructions(instructions, keys, code_options)
    return bytecode, tracer_output

