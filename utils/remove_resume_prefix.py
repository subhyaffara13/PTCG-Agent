
def remove_resume_prefix(name: str) -> str:
    from .resume_execution import TORCH_DYNAMO_RESUME_IN_PREFIX

    match = re.match(f"{TORCH_DYNAMO_RESUME_IN_PREFIX}_(\\w+)_at_\\d+", name)
    if match:
        return match.group(1)
    return name

