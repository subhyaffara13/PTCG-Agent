
def get_empty_usage() -> Usage:
    return Usage(
        prompt_tokens=0,
        completion_tokens=0,
        total_tokens=0,
    )

