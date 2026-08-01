
def get_timeout(test_id) -> int:
    return TIMEOUT_OVERRIDE.get(test_id.split(".")[-1], TIMEOUT_DEFAULT)

