
def compile_so(aoti_dir: str, aoti_files: list[str], so_path: str) -> str:
    def get_aoti_file_with_suffix(suffix: str) -> str:
        for file in aoti_files:
            if file.endswith(suffix):
                return file
        raise RuntimeError(f"Unable to find file with suffix {suffix}")

    # Compile all the files into a .so
    cpp_file = os.path.join(aoti_dir, get_aoti_file_with_suffix(".cpp"))
    consts_o = os.path.join(aoti_dir, get_aoti_file_with_suffix(".o"))

    file_name = os.path.splitext(cpp_file)[0]

    # Parse compile flags and build the .o file
    with open(file_name + "_compile_flags.json") as f:
        compile_flags = json.load(f)

    compile_options = BuildOptionsBase(
        **compile_flags, use_relative_path=config.is_fbcode()
    )
    object_builder = CppBuilder(
        name=file_name,
        sources=cpp_file,
        BuildOption=compile_options,
    )
    output_o = object_builder.get_target_file_path()
    object_builder.build()

    # Parse linker flags and build the .so file
    with open(file_name + "_linker_flags.json") as f:
        linker_flags = json.load(f)

    linker_options = BuildOptionsBase(
        **linker_flags, use_relative_path=config.is_fbcode()
    )
    so_builder = CppBuilder(
        name=os.path.split(so_path)[-1],
        sources=[output_o, consts_o],
        BuildOption=linker_options,
        output_dir=so_path,
    )
    output_so = so_builder.get_target_file_path()
    so_builder.build()

    # mmapped weights
    serialized_weights_filename = file_name + "_serialized_weights.bin"
    if serialized_weights_filename in aoti_files:
        with open(serialized_weights_filename, "rb") as f_weights:
            serialized_weights = f_weights.read()

        with open(output_so, "a+b") as f_so:
            so_size = f_so.tell()
            # Page align the weights
            f_so.write(b" " * (16384 - so_size % 16384))
            f_so.write(serialized_weights)

    return output_so

