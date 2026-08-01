
def _worker_compile_cpp(
    lock_path: str,
    cpp_builders: Sequence[CppBuilder],
) -> None:
    from torch.utils._filelock import FileLock

    with FileLock(lock_path, timeout=LOCK_TIMEOUT):
        for builder in cpp_builders:
            if not os.path.exists(builder.get_target_file_path()):
                builder.build()

