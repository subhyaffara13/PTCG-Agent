
def TruncateToFourByteFloat(original):
  return struct.unpack('<f', struct.pack('<f', original))[0]

