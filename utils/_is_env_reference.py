
def _is_env_reference(value: object) -> bool:
    return isinstance(value, str) and "os.environ/" in value

