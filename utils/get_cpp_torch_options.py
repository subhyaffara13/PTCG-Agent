
def get_cpp_torch_options(
    cpp_compiler: str,
    vec_isa: VecISA,
    include_pytorch: bool,
    aot_mode: bool,
    use_relative_path: bool,
    use_mmap_weights: bool,
    use_mmap_weights_external: bool,
) -> tuple[list[str], list[str], list[str], list[str], list[str], list[str], list[str]]:
    """
    This function is used to get the build args of torch related build options.
    1. Torch include_directories, libraries, libraries_directories.
    2. Python include_directories, libraries, libraries_directories.
    3. OpenMP related.
    4. Torch MACROs.
    5. MISC
    6. Return the build args
    """
    definitions: list[str] = []
    include_dirs: list[str] = []
    cflags: list[str] = []
    ldflags: list[str] = []
    libraries_dirs: list[str] = []
    libraries: list[str] = []
    passthrough_args: list[str] = []

    torch_cpp_wrapper_definitions = _get_torch_cpp_wrapper_definition()
    use_custom_generated_macros_definitions = _use_custom_generated_macros()

    (
        sys_libs_cflags,
        sys_libs_include_dirs,
        sys_libs_passthrough_args,
        sys_libs_ldflags,
    ) = _setup_standard_sys_libs(cpp_compiler, aot_mode, use_relative_path)

    isa_macros, isa_ps_args_build_flags = _get_build_args_of_chosen_isa(vec_isa)

    (
        torch_include_dirs,
        torch_libraries_dirs,
        torch_libraries,
    ) = _get_torch_related_args(include_pytorch=include_pytorch, aot_mode=aot_mode)

    python_include_dirs, python_libraries_dirs = _get_python_related_args()

    (
        omp_cflags,
        omp_ldflags,
        omp_include_dir_paths,
        omp_lib_dir_paths,
        omp_lib,
        omp_passthrough_args,
    ) = _get_openmp_args(cpp_compiler)

    fb_macro_passthrough_args = _use_fb_internal_macros()

    mmap_self_macros = get_mmap_self_macro(use_mmap_weights, use_mmap_weights_external)
    caching_allocator_macros = get_caching_allocator_macro()

    definitions = (
        torch_cpp_wrapper_definitions
        + use_custom_generated_macros_definitions
        + isa_macros
        + fb_macro_passthrough_args
        + mmap_self_macros
        + caching_allocator_macros
    )
    include_dirs = (
        sys_libs_include_dirs
        + python_include_dirs
        + torch_include_dirs
        + omp_include_dir_paths
    )
    cflags = sys_libs_cflags + omp_cflags
    ldflags = sys_libs_ldflags + omp_ldflags
    libraries_dirs = python_libraries_dirs + torch_libraries_dirs + omp_lib_dir_paths
    libraries = torch_libraries + omp_lib
    passthrough_args = (
        sys_libs_passthrough_args + isa_ps_args_build_flags + omp_passthrough_args
    )

    return (
        definitions,
        include_dirs,
        cflags,
        ldflags,
        libraries_dirs,
        libraries,
        passthrough_args,
    )

