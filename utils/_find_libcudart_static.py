
def _find_libcudart_static(path: str) -> Path | None:
    lib_dirs = list(Path(path).rglob("libcudart_static.a"))
    if lib_dirs:
        return lib_dirs[0].resolve().parent
    log_msg = f'"libcudart_static.a" not found under {path}'
    log.info(log_msg)
    return None

