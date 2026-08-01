
def _get_cuda_dep_paths(path: str, lib_folder: str, lib_name: str) -> list[str]:
    # Libraries can either be in
    # path/nvidia/lib_folder/lib or
    # path/nvidia/cuXX/lib (since CUDA 13.0) or
    # path/lib_folder/lib
    from torch.version import cuda as cuda_version

    nvidia_lib_paths = glob.glob(
        os.path.join(path, "nvidia", lib_folder, "lib", lib_name)
    )
    if cuda_version is not None:
        maj_cuda_version = cuda_version.split(".")[0]
        nvidia_lib_paths += glob.glob(
            os.path.join(path, "nvidia", f"cu{maj_cuda_version}", "lib", lib_name)
        )
    lib_paths = glob.glob(os.path.join(path, lib_folder, "lib", lib_name))

    return nvidia_lib_paths + lib_paths

