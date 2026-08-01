
def xmlToTag(tag: str) -> str:
    """The opposite of tagToXML()"""
    if tag == "OS_2":
        return Tag("OS/2")
    if len(tag) == 8:
        return identifierToTag(tag)
    else:
        return Tag(tag + " " * (4 - len(tag)))

