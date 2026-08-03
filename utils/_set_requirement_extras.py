import re

def _set_requirement_extras(req: Requirement, new_extras: set[str]) -> Requirement:
    """
    Returns a new requirement based on the given one, with the supplied extras. If the
    given requirement already has extras those are replaced (or dropped if no new extras
    are given).
    """
    match: re.Match[str] | None = re.fullmatch(
        # see https://peps.python.org/pep-0508/#complete-grammar
        r"([\w\t .-]+)(\[[^\]]*\])?(.*)",
        str(req),
        flags=re.ASCII,
    )
    # ireq.req is a valid requirement so the regex should always match
    assert (
        match is not None
    ), f"regex match on requirement {req} failed, this should never happen"
    pre: str | None = match.group(1)
    post: str | None = match.group(3)
    assert (
        pre is not None and post is not None
    ), f"regex group selection for requirement {req} failed, this should never happen"
    extras: str = "[{}]".format(",".join(sorted(new_extras)) if new_extras else "")
    return get_requirement(f"{pre}{extras}{post}")

