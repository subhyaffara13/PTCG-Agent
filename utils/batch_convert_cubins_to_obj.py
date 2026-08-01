
def batch_convert_cubins_to_obj(
    cubins: list[tuple[str, str]],
    output_dir: str,
    cpp_compiler: str = "gcc",
) -> str:
    """Convert multiple cubin files to a single .o using batched .incbin assembly.

    Instead of spawning 3 subprocesses per cubin (ld + 2x objcopy), generates
    a single .S file with .incbin directives for all cubins and compiles it
    with one compiler invocation. Produces bit-identical rodata and symbols
    as the per-cubin convert_cubin_to_obj approach.

    Args:
        cubins: list of (cubin_file_path, kernel_name) tuples.
        output_dir: directory for the generated .S and .o files.
        cpp_compiler: C compiler to use for assembling (default: gcc).

    Returns:
        Path to the combined .o file.
    """
    asm_path = os.path.join(output_dir, "cubins_combined.S")
    obj_path = os.path.join(output_dir, "cubins_combined.o")

    with open(asm_path, "w") as f:
        f.write(".section .rodata\n")
        for cubin_file, kernel_name in cubins:
            # Use absolute path to avoid issues with working directory
            abs_cubin = os.path.abspath(cubin_file)
            escaped_path = abs_cubin.replace("\\", "\\\\").replace('"', '\\"')
            f.write(
                f".balign 16\n"
                f".global __{kernel_name}_start\n"
                f".global __{kernel_name}_end\n"
                f"__{kernel_name}_start:\n"
                f'.incbin "{escaped_path}"\n'
                f"__{kernel_name}_end:\n"
                f".global __{kernel_name}_size\n"
                f".set __{kernel_name}_size, "
                f"__{kernel_name}_end - __{kernel_name}_start\n"
            )

    subprocess.run(
        [cpp_compiler, "-c", asm_path, "-o", obj_path],
        capture_output=True,
        text=True,
        check=True,
    )
    return obj_path

