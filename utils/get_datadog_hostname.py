
def get_datadog_hostname() -> str:
    return os.getenv("HOSTNAME", "")

