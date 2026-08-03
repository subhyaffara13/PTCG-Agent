import sys

def decoding_stream(
    stream: BufferedReader | BytesIO,
    encoding: str,
    errors: Literal["strict"] = "strict",
) -> codecs.StreamReader:
    try:
        reader_cls = codecs.getreader(encoding or sys.getdefaultencoding())
    except LookupError:
        reader_cls = codecs.getreader(sys.getdefaultencoding())
    return reader_cls(stream, errors)

