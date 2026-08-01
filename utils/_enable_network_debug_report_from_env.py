
def _enable_network_debug_report_from_env() -> bool:
    enabled, output_path = _parse_network_debug_env()
    if not enabled:
        return False

    _enable_network_debug_report(output_path=output_path)
    return True

