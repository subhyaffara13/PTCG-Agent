
def _sycl_compiler_options() -> list[str]:
    options = [
        "-DCUTLASS_ENABLE_SYCL",
        "-DSYCL_INTEL_TARGET",
        "-DCUTLASS_VERSIONS_GENERATED",
        "-O3",
        "-DNDEBUG",
        "-std=c++20",
        "-fPIC",
        "-fsycl",
        f"-fsycl-targets={_sycl_arch_as_compile_option()}",
        "-Xspirv-translator",
        "-spirv-ext=+SPV_INTEL_split_barrier,+SPV_INTEL_2d_block_io,+SPV_INTEL_subgroup_matrix_multiply_accumulate",
        "-fno-sycl-instrument-device-code",
        "-DMKL_ILP64",
        "-MD",
        "-MT",
    ]
    if config.cutlass.enable_debug_info:
        options.extend(["-lineinfo", "-g", "-DCUTLASS_DEBUG_TRACE_LEVEL=1"])
    return options

