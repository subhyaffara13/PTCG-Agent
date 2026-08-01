
def _Unpack(fmt, buf):
  return struct.unpack('<%s' % fmt[len(buf)], buf)[0]

