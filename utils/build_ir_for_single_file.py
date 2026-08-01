
def build_ir_for_single_file(
    input_lines: list[str], compiler_options: CompilerOptions | None = None
) -> list[FuncIR]:
    return build_ir_for_single_file2(input_lines, compiler_options)[0].functions

