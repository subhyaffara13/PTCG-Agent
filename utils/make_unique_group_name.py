
def makeUniqueGroupName(name: str, groupNames: list[str], counter: int = 0) -> str:
    """Make a kerning group name that will be unique within the set of group names.

    If the requested kerning group name already exists within the set, this
    will return a new name by adding an incremented counter to the end
    of the requested name.

    Args:
        name:
          The requested kerning group name.
        groupNames:
          A list of the existing kerning group names.
        counter:
          Optional; a counter of group names already seen (default: 0). If
          :attr:`.counter` is not provided, the function will recurse,
          incrementing the value of :attr:`.counter` until it finds the
          first unused ``name+counter`` combination, and return that result.

    Returns:
        A unique kerning group name composed of the requested name suffixed
        by the smallest available integer counter.
    """
    # Add a number to the name if the counter is higher than zero.
    newName = name
    if counter > 0:
        newName = "%s%d" % (newName, counter)
    # If the new name is in the existing group names, recurse.
    if newName in groupNames:
        return makeUniqueGroupName(name, groupNames, counter + 1)
    # Otherwise send back the new name.
    return newName

