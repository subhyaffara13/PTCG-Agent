
def _should_fill(lname, rname) -> bool:
    if not isinstance(lname, str) or not isinstance(rname, str):
        return True
    return lname == rname

