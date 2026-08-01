
def _rocm_lib_options(dst_file_ext: str) -> list[str]:
    from torch.utils import cpp_extension

    rocm_lib_dir = (
        os.path.join(config.rocm.rocm_home, "lib")
        if config.rocm.rocm_home
        else cpp_extension._join_rocm_home("lib")
    )
    hip_lib_dir = (
        os.path.join(config.rocm.rocm_home, "hip", "lib")
        if config.rocm.rocm_home
        else cpp_extension._join_rocm_home("hip", "lib")
    )

    opts = [
        "-include __clang_hip_runtime_wrapper.h",
        f"-L{os.path.realpath(rocm_lib_dir)}",
        f"-L{os.path.realpath(hip_lib_dir)}",
        "-lamdhip64",
    ]
    if dst_file_ext == "exe":
        opts += ["-lpthread", "-lstdc++"]
    return opts

