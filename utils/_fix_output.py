
def _fix_output(output, usemask=True, asrecarray=False):
    """
    Private function: return a recarray, an ndarray, a MaskedArray
    or a MaskedRecords depending on the input parameters
    """
    if not isinstance(output, ma.MaskedArray):
        usemask = False
    if usemask:
        if asrecarray:
            output = output.view(mrec.MaskedRecords)
    else:
        output = ma.filled(output)
        if asrecarray:
            output = output.view(np.recarray)
    return output

