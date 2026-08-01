
def default_debug_dir_root() -> str:
    # [@compile_ignored: debug]
    DEBUG_DIR_VAR_NAME = "TORCH_COMPILE_DEBUG_DIR"
    if DEBUG_DIR_VAR_NAME in os.environ:
        return os.path.join(os.environ[DEBUG_DIR_VAR_NAME], "torch_compile_debug")
    elif is_fbcode():
        return os.path.join(
            tempfile.gettempdir(), getpass.getuser(), "torch_compile_debug"
        )
    else:
        return os.path.join(os.getcwd(), "torch_compile_debug")

