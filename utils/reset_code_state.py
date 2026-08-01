
def reset_code_state() -> None:
    global _CODE_STATE, _INIT_CODE_STATE, _LOGGED_DYNAMIC_ALLOWLIST
    _CODE_STATE = None
    _INIT_CODE_STATE = None
    _LOGGED_DYNAMIC_ALLOWLIST = False

