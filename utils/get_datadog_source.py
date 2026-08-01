
def get_datadog_source() -> str:
    return os.getenv("DD_SOURCE", "litellm")

