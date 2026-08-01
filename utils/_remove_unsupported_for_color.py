
def _removeUnsupportedForColor(dataFunctions):
    dataFunctions = dict(dataFunctions)
    del dataFunctions["row"]
    return dataFunctions

