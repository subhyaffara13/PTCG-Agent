
def _get_use_created() -> bool:
    return os.environ.get("PROMETHEUS_DISABLE_CREATED_SERIES", 'False').lower() not in ('true', '1', 't')

