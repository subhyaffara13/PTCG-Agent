
def aoti_eager_op_conf_lock(op_func_name_with_overload: str) -> Any:
    # Avoid circular import
    from torch._inductor.codecache import get_lock_dir, LOCK_TIMEOUT
    from torch.utils._filelock import FileLock

    op_conf_lock_file = f"{op_func_name_with_overload}.lock"
    lock_dir = get_lock_dir()
    return FileLock(os.path.join(lock_dir, op_conf_lock_file), timeout=LOCK_TIMEOUT)

