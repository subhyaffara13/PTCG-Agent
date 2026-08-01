
def _transform_cuda_paths(lpaths: list[str]) -> None:
    # This handles two cases:
    # 1. Cases where libs are in (e.g.) lib/cuda-12 and lib/cuda-12/stubs
    # 2. Linux machines may have CUDA installed under either lib64/ or lib/
    for i, path in enumerate(lpaths):
        if "CUDA_HOME" in os.environ and path.startswith(os.environ["CUDA_HOME"]):
            lib_dir: Path | None = _find_libcudart_static(path)
            if lib_dir is None:
                continue
            lpaths[i] = str(lib_dir)
            stub_dir = lib_dir / "stubs"
            if stub_dir.exists():
                lpaths.append(str(stub_dir))

