
def convertUFO1OrUFO2KerningToUFO3Kerning(
    kerning: KerningNested, groups: dict[str, list[str]], glyphSet: Container[str] = ()
) -> tuple[KerningNested, dict[str, list[str]], dict[str, dict[str, str]]]:
    """Convert kerning data in UFO1 or UFO2 syntax into UFO3 syntax.

    Args:
      kerning:
          A dictionary containing the kerning rules defined in
          the UFO font, as used in :class:`.UFOReader` objects.
      groups:
          A dictionary containing the groups defined in the UFO
          font, as used in :class:`.UFOReader` objects.
      glyphSet:
        Optional; a set of glyph objects to skip (default: None).

    Returns:
      1. A dictionary representing the converted kerning data.
      2. A copy of the groups dictionary, with all groups renamed to UFO3 syntax.
      3. A dictionary containing the mapping of old group names to new group names.

    """
    # gather known kerning groups based on the prefixes
    firstReferencedGroups, secondReferencedGroups = findKnownKerningGroups(groups)
    # Make lists of groups referenced in kerning pairs.
    for first, seconds in list(kerning.items()):
        if first in groups and first not in glyphSet:
            if not first.startswith("public.kern1."):
                firstReferencedGroups.add(first)
        for second in list(seconds.keys()):
            if second in groups and second not in glyphSet:
                if not second.startswith("public.kern2."):
                    secondReferencedGroups.add(second)
    # Create new names for these groups.
    firstRenamedGroups: dict[str, str] = {}
    for first in firstReferencedGroups:
        # Make a list of existing group names.
        existingGroupNames = list(groups.keys()) + list(firstRenamedGroups.keys())
        # Remove the old prefix from the name
        newName = first.replace("@MMK_L_", "")
        # Add the new prefix to the name.
        newName = "public.kern1." + newName
        # Make a unique group name.
        newName = makeUniqueGroupName(newName, existingGroupNames)
        # Store for use later.
        firstRenamedGroups[first] = newName
    secondRenamedGroups: dict[str, str] = {}
    for second in secondReferencedGroups:
        # Make a list of existing group names.
        existingGroupNames = list(groups.keys()) + list(secondRenamedGroups.keys())
        # Remove the old prefix from the name
        newName = second.replace("@MMK_R_", "")
        # Add the new prefix to the name.
        newName = "public.kern2." + newName
        # Make a unique group name.
        newName = makeUniqueGroupName(newName, existingGroupNames)
        # Store for use later.
        secondRenamedGroups[second] = newName
    # Populate the new group names into the kerning dictionary as needed.
    newKerning = {}
    for first, seconds in list(kerning.items()):
        first = firstRenamedGroups.get(first, first)
        newSeconds = {}
        for second, value in list(seconds.items()):
            second = secondRenamedGroups.get(second, second)
            newSeconds[second] = value
        newKerning[first] = newSeconds
    # Make copies of the referenced groups and store them
    # under the new names in the overall groups dictionary.
    allRenamedGroups = list(firstRenamedGroups.items())
    allRenamedGroups += list(secondRenamedGroups.items())
    for oldName, newName in allRenamedGroups:
        group = list(groups[oldName])
        groups[newName] = group
    # Return the kerning and the groups.
    return newKerning, groups, dict(side1=firstRenamedGroups, side2=secondRenamedGroups)

