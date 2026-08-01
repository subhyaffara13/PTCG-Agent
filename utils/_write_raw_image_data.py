
def _writeRawImageData(strikeIndex, glyphName, bitmapObject, writer, ttFont):
    writer.begintag("rawimagedata")
    writer.newline()
    writer.dumphex(bitmapObject.imageData)
    writer.endtag("rawimagedata")
    writer.newline()

