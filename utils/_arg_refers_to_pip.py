
def _arg_refers_to_pip(arg: str) -> bool:
    try:
        req = Requirement(arg)
    except InvalidRequirement:
        return False
    return canonicalize_name(req.name) == "pip"

