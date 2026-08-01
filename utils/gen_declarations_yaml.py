
def gen_declarations_yaml(
    cpu_fm: FileManager, native_functions: Sequence[NativeFunction]
) -> None:
    cpu_fm.write(
        "Declarations.yaml",
        lambda: format_yaml([compute_declaration_yaml(f) for f in native_functions]),
    )

