
def process_env_var_string_for_windows(env_var_str: str) -> str:
    """
    When we setup logging config as guide: https://docs.pytorch.org/docs/stable/logging.html
    Such as:
        TORCH_LOGS="+schedule,+inductor,+output_code"

    On Linux, it shows as:
        declare -x SSH_TTY="/dev/pts/0"
        declare -x TERM="xterm"
        declare -x TORCH_LOGS="+schedule,+inductor,+output_code"
        declare -x USER="xu"

    On Windows, it shows as:
        TORCHINDUCTOR_WINDOWS_TESTS=1
        TORCH_LOGS="+schedule,+inductor,+output_code"
        UCRTVersion=10.0.22000.0

    For Linux, it shows quotes by default, And Windows is not shows quotes.
    Besides that, Windows would auto assemble quotes when env var processing.
    On Linux, we will get variable: "+schedule,+inductor,+output_code"
    On Windows, we will get variable: '"+schedule,+inductor,+output_code"'

    So, we need remove the outer quotes for Windows.
    """
    _IS_WINDOWS = sys.platform == "win32"

    def remove_outer_quotes(s: str) -> str:
        if len(s) >= 2 and (
            (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")
        ):
            return s[1:-1]
        return s

    if _IS_WINDOWS:
        env_var_str = remove_outer_quotes(env_var_str)

    return env_var_str

