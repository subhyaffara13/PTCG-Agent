import os

def _setup_standard_sys_libs(
    cpp_compiler: str,
    aot_mode: bool,
    use_relative_path: bool,
) -> tuple[list[str], list[str], list[str], list[str]]:
    cflags: list[str] = []
    include_dirs: list[str] = []
    passthrough_args: list[str] = []
    ldflags: list[str] = []
    if _IS_WINDOWS:
        return cflags, include_dirs, passthrough_args, ldflags

    if config.is_fbcode():
        # TODO(T203137008) Can we unify these flags with triton_cc_command?
        cflags.append("nostdinc")
        # Note that the order of include paths do matter, as a result
        # we need to have several branches interleaved here
        include_dirs.append(build_paths.sleef_include)
        include_dirs.append(build_paths.openmp_include)
        include_dirs.append(build_paths.python_include)
        include_dirs.append(build_paths.cc_include)
        include_dirs.append(build_paths.libgcc_include)
        include_dirs.append(build_paths.libgcc_arch_include)
        include_dirs.append(build_paths.libgcc_backward_include)
        include_dirs.append(build_paths.glibc_include)
        include_dirs.append(build_paths.linux_kernel_include)
        include_dirs.append("include")

        if aot_mode and not use_relative_path:
            linker_script = _LINKER_SCRIPT
        else:
            linker_script = os.path.basename(_LINKER_SCRIPT)

        if _is_clang(cpp_compiler):
            passthrough_args.append(" --rtlib=compiler-rt")
            passthrough_args.append(" -B" + build_paths.glibc_lib)
            ldflags.append("fuse-ld=lld")
            ldflags.append(f"Wl,--script={linker_script}")
            ldflags.append("L" + build_paths.glibc_lib)

    return cflags, include_dirs, passthrough_args, ldflags

