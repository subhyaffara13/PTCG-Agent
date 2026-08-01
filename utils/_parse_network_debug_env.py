
def _parse_network_debug_env() -> tuple[bool, str]:
    enabled_raw = os.environ.get("NETWORK_DEBUG_REPORT", "").strip()
    try:
        enabled = bool(strtobool(enabled_raw)) if enabled_raw else False
    except ValueError:
        enabled = False

    output_path = os.environ.get("NETWORK_DEBUG_REPORT_PATH", "").strip() or _DEFAULT_REPORT_PATH
    return enabled, output_path

