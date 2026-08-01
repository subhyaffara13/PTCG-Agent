
def _has_option(options: Values, reqs: list[InstallRequirement], option: str) -> bool:
    if getattr(options, option, None):
        return True
    for req in reqs:
        if getattr(req, option, None):
            return True
    return False

