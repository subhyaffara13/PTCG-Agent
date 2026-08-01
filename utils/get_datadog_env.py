
def get_datadog_env() -> str:
    return os.getenv("DD_ENV", "unknown")

