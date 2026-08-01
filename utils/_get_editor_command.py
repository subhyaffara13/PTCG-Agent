
def _get_editor_command() -> str | None:
    for env in ("HF_EDITOR", "VISUAL", "EDITOR"):
        if command := os.getenv(env, "").strip():
            return command
    for binary_path, editor_command in PREFERRED_EDITORS:
        if shutil.which(binary_path) is not None:
            return editor_command
    return None

