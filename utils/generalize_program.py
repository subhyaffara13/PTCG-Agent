
def generalizeProgram(program, getNumRegions=None, **kwargs):
    return commandsToProgram(
        generalizeCommands(programToCommands(program, getNumRegions), **kwargs)
    )

