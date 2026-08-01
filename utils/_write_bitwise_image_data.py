
def _writeBitwiseImageData(strikeIndex, glyphName, bitmapObject, writer, ttFont):
    metrics = bitmapObject.exportMetrics
    del bitmapObject.exportMetrics
    bitDepth = bitmapObject.exportBitDepth
    del bitmapObject.exportBitDepth

    # A dict for mapping binary to more readable/artistic ASCII characters.
    binaryConv = {"0": ".", "1": "@"}

    writer.begintag(
        "bitwiseimagedata",
        bitDepth=bitDepth,
        width=metrics.width,
        height=metrics.height,
    )
    writer.newline()
    for curRow in range(metrics.height):
        rowData = bitmapObject.getRow(
            curRow, bitDepth=1, metrics=metrics, reverseBytes=True
        )
        rowData = _data2binary(rowData, metrics.width)
        # Make the output a readable ASCII art form.
        rowData = strjoin(map(binaryConv.get, rowData))
        writer.simpletag("row", value=rowData)
        writer.newline()
    writer.endtag("bitwiseimagedata")
    writer.newline()

