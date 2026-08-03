import sys

def _make_readerlike(stream, byte_order=boc.native_code):
    class R:
        pass
    r = R()
    r.mat_stream = stream
    r.byte_order = byte_order
    r.struct_as_record = True
    r.uint16_codec = sys.getdefaultencoding()
    r.chars_as_strings = False
    r.mat_dtype = False
    r.squeeze_me = False
    return r

