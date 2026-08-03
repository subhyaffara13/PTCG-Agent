import os

def _manager_path():
    if platform.system() == "Windows":
        return b""
    path = get_file_path("torch", "bin", "torch_shm_manager")
    prepare_multiprocessing_environment(get_file_path("torch"))
    if not os.path.exists(path):
        raise RuntimeError("Unable to find torch_shm_manager at " + path)
    return path.encode("utf-8")

