
def run_asm_build_object(src: str, target: str, cwd: str) -> None:
    def get_asm_compiler() -> str:
        if _IS_WINDOWS:
            ASM_CC = "ml64"
        else:
            ASM_CC = get_cpp_compiler()
            # Intel compiler is not support to compile asm, switch to gcc.
            if _is_intel_compiler(ASM_CC):
                ASM_CC = "gcc"
        return ASM_CC

    def get_command_line(asm_cc: str, src: str, target: str) -> str:
        if _IS_WINDOWS:
            # Format reference:
            # https://learn.microsoft.com/en-us/cpp/assembler/masm/ml-and-ml64-command-line-reference?view=msvc-170
            cmd = f"{asm_cc} {src} /c /Fo {target}"  # codespell:ignore /Fo
        else:
            cmd = f"{asm_cc} -c {src} -o {target}"

        return cmd

    asm_cc = get_asm_compiler()
    cmd = get_command_line(
        asm_cc=asm_cc,
        src=normalize_path_separator(src),
        target=normalize_path_separator(target),
    )
    run_compile_cmd(cmd, cwd=normalize_path_separator(cwd))

