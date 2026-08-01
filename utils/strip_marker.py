
def strip_marker(req) -> packaging.requirements.Requirement:
    """
    Return a new requirement without the environment marker to avoid
    calling pip with something like `babel; extra == "i18n"`, which
    would always be ignored.
    """
    # create a copy to avoid mutating the input
    req = packaging.requirements.Requirement(str(req))
    req.marker = None
    return req

