import os

def _update_log_state_from_env() -> None:
    global log_state
    log_setting = os.environ.get(LOG_ENV_VAR, None)
    if log_setting is not None:
        log_state = _parse_log_settings(log_setting)

