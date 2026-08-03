from typing import Optional, Set

def convert_extras(extras: Optional[str]) -> Set[str]:
    if not extras:
        return set()
    return Requirement("placeholder" + extras.lower()).extras


def convert_extras(extras: str | None) -> set[str]:
    if not extras:
        return set()
    return get_requirement("placeholder" + extras.lower()).extras

