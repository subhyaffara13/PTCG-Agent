
def specializeProgram(program, getNumRegions=None, **kwargs):
    return commandsToProgram(
        specializeCommands(programToCommands(program, getNumRegions), **kwargs)
    )

