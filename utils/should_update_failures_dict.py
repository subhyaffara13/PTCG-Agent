
def should_update_failures_dict() -> bool:
    key = "PYTORCH_OPCHECK_ACCEPT"
    return key in os.environ and os.environ[key] == "1"

