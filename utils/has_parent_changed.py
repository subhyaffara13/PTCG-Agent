
def has_parent_changed() -> bool:
    return _original_parent != os.getppid()

