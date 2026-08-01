
def get_datadog_pod_name() -> str:
    return os.getenv("POD_NAME", "unknown")

