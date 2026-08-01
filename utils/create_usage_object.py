
def create_usage_object(usage):
    usage_dict = {}

    if usage.completion_tokens is not None:
        usage_dict["completion_tokens"] = usage.completion_tokens
    if usage.prompt_tokens is not None:
        usage_dict["prompt_tokens"] = usage.prompt_tokens
    if usage.total_tokens is not None:
        usage_dict["total_tokens"] = usage.total_tokens
    return usage_dict

