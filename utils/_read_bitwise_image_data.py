
def _readBitwiseImageData(bitmapObject, name, attrs, content, ttFont):
    bitDepth = safeEval(attrs["bitDepth"])
    metrics = SmallGlyphMetrics()
    metrics.width = safeEval(attrs["width"])
    metrics.height = safeEval(attrs["height"])

    # A dict for mapping from ASCII to binary. All characters are considered
    # a '1' except space, period and '0' which maps to '0'.
    binaryConv = {" ": "0", ".": "0", "0": "0"}

    dataRows = []
    for element in content:
        if not isinstance(element, tuple):
            continue
        name, attr, content = element
        if name == "row":
            mapParams = zip(attr["value"], itertools.repeat("1"))
            rowData = strjoin(itertools.starmap(binaryConv.get, mapParams))
            dataRows.append(_binary2data(rowData))

    bitmapObject.setRows(
        dataRows, bitDepth=bitDepth, metrics=metrics, reverseBytes=True
    )

