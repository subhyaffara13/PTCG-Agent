import os

def print_loaded_libraries(cuda_related_only=True):
    import psutil  # noqa: PLC0415

    p = psutil.Process(os.getpid())
    for lib in p.memory_maps():
        if (not cuda_related_only) or any(x in lib.path for x in ("libcu", "libnv", "tensorrt")):
            print(lib.path)

