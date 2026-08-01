
def _DoubleDecoder():
  """Returns a decoder for a double field.

  This code works around a bug in struct.unpack for not-a-number.
  """

  local_unpack = struct.unpack

  def InnerDecode(buffer, pos):
    """Decode serialized double to a double and new position.

    Args:
      buffer: memoryview of the serialized bytes.
      pos: int, position in the memory view to start at.

    Returns:
      Tuple[float, int] of the decoded double value and new position
      in the serialized data.
    """
    # We expect a 64-bit value in little-endian byte order.  Bit 1 is the sign
    # bit, bits 2-12 represent the exponent, and bits 13-64 are the significand.
    new_pos = pos + 8
    double_bytes = buffer[pos:new_pos].tobytes()

    # If this value has all its exponent bits set and at least one significand
    # bit set, it's not a number.  In Python 2.4, struct.unpack will treat it
    # as inf or -inf.  To avoid that, we treat it specially.
    if ((double_bytes[7:8] in b'\x7F\xFF')
        and (double_bytes[6:7] >= b'\xF0')
        and (double_bytes[0:7] != b'\x00\x00\x00\x00\x00\x00\xF0')):
      return (math.nan, new_pos)

    # Note that we expect someone up-stack to catch struct.error and convert
    # it to _DecodeError -- this way we don't have to set up exception-
    # handling blocks every time we parse one value.
    result = local_unpack('<d', double_bytes)[0]
    return (result, new_pos)
  return _SimpleDecoder(wire_format.WIRETYPE_FIXED64, InnerDecode)

