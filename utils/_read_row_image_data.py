
def _readRowImageData(bitmapObject, name, attrs, content, ttFont):
    bitDepth = safeEval(attrs["bitDepth"])
    metrics = SmallGlyphMetrics()
    metrics.width = safeEval(attrs["width"])
    metrics.height = safeEval(attrs["height"])

    dataRows = []
    for element in content:
        if not isinstance(element, tuple):
            continue
        name, attr, content = element
        # Chop off 'imagedata' from the tag to get just the option.
        if name == "row":
            dataRows.append(deHexStr(attr["value"]))
    bitmapObject.setRows(dataRows, bitDepth=bitDepth, metrics=metrics)

