
def get_datadog_service() -> str:
    return os.getenv("DD_SERVICE", "litellm-server")

