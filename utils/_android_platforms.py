import re

def _android_platforms(arch: str) -> list[str]:
    match = re.fullmatch(r"android_(\d+)_(.+)", arch)
    if match:
        api_level, abi = match.groups()
        return list(android_platforms(int(api_level), abi))
    else:
        # arch pattern didn't match (?!)
        return [arch]

