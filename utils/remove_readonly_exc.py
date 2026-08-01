
def remove_readonly_exc(func: Callable[..., object], path: str, exc: Exception) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)

