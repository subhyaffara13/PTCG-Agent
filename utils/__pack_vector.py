
def _PackVector(fmt, values, byte_width):
  return struct.pack('<%d%s' % (len(values), fmt[byte_width]), *values)

