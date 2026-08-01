
def _makeDict(
    instructionList: list[tuple[int, str, int, str, int, int]],
) -> tuple[dict, dict]:
    opcodeDict = {}
    mnemonicDict = {}
    for op, mnemonic, argBits, name, pops, pushes in instructionList:
        assert _mnemonicPat.match(mnemonic)
        mnemonicDict[mnemonic] = op, argBits, name
        if argBits:
            argoffset = op
            for i in range(1 << argBits):
                opcodeDict[op + i] = mnemonic, argBits, argoffset, name
        else:
            opcodeDict[op] = mnemonic, 0, 0, name
    return opcodeDict, mnemonicDict

