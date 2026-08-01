
def instantiateCFF2(
    varfont,
    axisLimits,
    *,
    round=round,
    specialize=True,
    generalize=False,
    downgrade=False,
):
    # The algorithm here is rather simple:
    #
    # Take all blend operations and store their deltas in the (otherwise empty)
    # CFF2 VarStore. Then, instantiate the VarStore with the given axis limits,
    # and read back the new deltas. This is done for both the CharStrings and
    # the Private dicts.
    #
    # Then prune unused things and possibly drop the VarStore if it's empty.
    #
    # If the downgrade parameter is True, no actual downgrading is done, but
    # the function returns True if the VarStore was empty after instantiation,
    # and hence a downgrade to CFF is possible. In all other cases it returns
    # False.

    log.info("Instantiating CFF2 table")

    fvarAxes = varfont["fvar"].axes

    cff = varfont["CFF2"].cff
    topDict = cff.topDictIndex[0]
    varStore = topDict.VarStore.otVarStore
    if not varStore:
        if downgrade:
            from fontTools.cffLib.CFF2ToCFF import convertCFF2ToCFF

            convertCFF2ToCFF(varfont)
        return

    cff.desubroutinize()

    def getNumRegions(vsindex):
        return varStore.VarData[vsindex if vsindex is not None else 0].VarRegionCount

    charStrings = topDict.CharStrings.values()

    # Gather all unique private dicts
    uniquePrivateDicts = set()
    privateDicts = []
    for fd in topDict.FDArray:
        if fd.Private not in uniquePrivateDicts:
            uniquePrivateDicts.add(fd.Private)
            privateDicts.append(fd.Private)

    allCommands = []
    allCommandPrivates = []
    for cs in charStrings:
        assert cs.private.vstore.otVarStore is varStore  # Or in many places!!
        commands = programToCommands(cs.program, getNumRegions=getNumRegions)
        if generalize:
            commands = generalizeCommands(commands)
        if specialize:
            commands = specializeCommands(commands, generalizeFirst=not generalize)
        allCommands.append(commands)
        allCommandPrivates.append(cs.private)

    def storeBlendsToVarStore(arg):
        if not isinstance(arg, list):
            return

        if any(isinstance(subarg, list) for subarg in arg[:-1]):
            raise NotImplementedError("Nested blend lists not supported (yet)")

        count = arg[-1]
        assert (len(arg) - 1) % count == 0
        nRegions = (len(arg) - 1) // count - 1
        assert nRegions == getNumRegions(vsindex)
        for i in range(count, len(arg) - 1, nRegions):
            deltas = arg[i : i + nRegions]
            assert len(deltas) == nRegions
            varData = varStore.VarData[vsindex]
            varData.Item.append(deltas)
            varData.ItemCount += 1

    def fetchBlendsFromVarStore(arg):
        if not isinstance(arg, list):
            return [arg]

        if any(isinstance(subarg, list) for subarg in arg[:-1]):
            raise NotImplementedError("Nested blend lists not supported (yet)")

        count = arg[-1]
        assert (len(arg) - 1) % count == 0
        numRegions = getNumRegions(vsindex)
        newDefaults = []
        newDeltas = []
        for i in range(count):
            defaultValue = arg[i]

            major = vsindex
            minor = varDataCursor[major]
            varDataCursor[major] += 1

            defaultValue += round(defaultDeltas[major][minor])
            newDefaults.append(defaultValue)

            varData = varStore.VarData[major]
            deltas = varData.Item[minor]
            assert len(deltas) == numRegions
            newDeltas.extend(deltas)

        if not numRegions:
            return newDefaults  # No deltas, just return the defaults

        return [newDefaults + newDeltas + [count]]

    # Check VarData's are empty
    for varData in varStore.VarData:
        assert varData.Item == []
        assert varData.ItemCount == 0

    # Add charstring blend lists to VarStore so we can instantiate them
    for commands, private in zip(allCommands, allCommandPrivates):
        vsindex = getattr(private, "vsindex", 0)
        for command in commands:
            if command[0] == "vsindex":
                vsindex = command[1][0]
                continue
            for arg in command[1]:
                storeBlendsToVarStore(arg)

    # Add private blend lists to VarStore so we can instantiate values
    for opcode, name, arg_type, default, converter in privateDictOperators2:
        if arg_type not in ("number", "delta", "array"):
            continue

        vsindex = 0
        for private in privateDicts:
            if not hasattr(private, name):
                continue
            values = getattr(private, name)

            # This is safe here since "vsindex" is the first in the privateDictOperators2
            if name == "vsindex":
                vsindex = values[0]
                continue

            if arg_type == "number":
                values = [values]

            for value in values:
                if not isinstance(value, list):
                    continue

                assert len(value) % (getNumRegions(vsindex) + 1) == 0
                count = len(value) // (getNumRegions(vsindex) + 1)
                storeBlendsToVarStore(value + [count])

    # Instantiate VarStore
    defaultDeltas = instantiateItemVariationStore(
        varStore, fvarAxes, axisLimits, hierarchical=True
    )

    # Read back new charstring blends from the instantiated VarStore
    varDataCursor = [0] * len(varStore.VarData)
    for commands, private in zip(allCommands, allCommandPrivates):
        vsindex = getattr(private, "vsindex", 0)
        for command in commands:
            if command[0] == "vsindex":
                vsindex = command[1][0]
                continue
            newArgs = []
            for arg in command[1]:
                newArgs.extend(fetchBlendsFromVarStore(arg))
            command[1][:] = newArgs

    # Read back new private blends from the instantiated VarStore
    for opcode, name, arg_type, default, converter in privateDictOperators2:
        if arg_type not in ("number", "delta", "array"):
            continue

        vsindex = 0
        for private in privateDicts:
            if not hasattr(private, name):
                continue

            # This is safe here since "vsindex" is the first in the privateDictOperators2
            if name == "vsindex":
                vsindex = values[0]
                continue

            values = getattr(private, name)
            if arg_type == "number":
                values = [values]

            newValues = []
            for value in values:
                if not isinstance(value, list):
                    newValues.append(value)
                    continue

                value.append(1)
                value = fetchBlendsFromVarStore(value)
                newValues.extend(v[:-1] if isinstance(v, list) else v for v in value)

            if arg_type == "number":
                newValues = newValues[0]

            setattr(private, name, newValues)

    # Empty out the VarStore
    for i, varData in enumerate(varStore.VarData):
        assert varDataCursor[i] == varData.ItemCount, (
            varDataCursor[i],
            varData.ItemCount,
        )
        varData.Item = []
        varData.ItemCount = 0

    # Collect surviving vsindexes
    usedVsindex = set(
        i for i in range(len(varStore.VarData)) if varStore.VarData[i].VarRegionCount
    )
    # Remove vsindex commands that are no longer needed
    for commands, private in zip(allCommands, allCommandPrivates):
        if not any(isinstance(arg, list) for command in commands for arg in command[1]):
            commands[:] = [command for command in commands if command[0] != "vsindex"]

    # Remove unused VarData and update vsindex values
    vsindexMapping = {v: i for i, v in enumerate(sorted(usedVsindex))}
    varStore.VarData = [
        varData for i, varData in enumerate(varStore.VarData) if i in usedVsindex
    ]
    varStore.VarDataCount = len(varStore.VarData)
    for commands in allCommands:
        for command in commands:
            if command[0] == "vsindex":
                command[1][0] = vsindexMapping[command[1][0]]
    for private in privateDicts:
        if hasattr(private, "vsindex"):
            private.vsindex = vsindexMapping[private.vsindex]

    # Remove initial vsindex commands that are implied
    for commands, private in zip(allCommands, allCommandPrivates):
        vsindex = getattr(private, "vsindex", 0)
        if commands and commands[0] == ("vsindex", [vsindex]):
            commands.pop(0)

    # Ship the charstrings!
    for cs, commands in zip(charStrings, allCommands):
        cs.program = commandsToProgram(commands)

    # Remove empty VarStore
    if not varStore.VarData:
        if "VarStore" in topDict.rawDict:
            del topDict.rawDict["VarStore"]
        del topDict.VarStore
        del topDict.CharStrings.varStore
        for private in privateDicts:
            del private.vstore

        if downgrade:
            return True

    return False

