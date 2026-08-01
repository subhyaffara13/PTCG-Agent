
def _VarintDecoder(mask, result_type):
  """Return an encoder for a basic varint value (does not include tag).

  Decoded values will be bitwise-anded with the given mask before being
  returned, e.g. to limit them to 32 bits.  The returned decoder does not
  take the usual "end" parameter -- the caller is expected to do bounds checking
  after the fact (often the caller can defer such checking until later).  The
  decoder returns a (value, new_pos) pair.
  """

  def DecodeVarint(buffer, pos: int=None):
    result = 0
    shift = 0
    while 1:
      if pos is None:
        # Read from BytesIO
        try:
          b = buffer.read(1)[0]
        except IndexError as e:
          if shift == 0:
            # End of BytesIO.
            return None
          else:
            raise ValueError('Fail to read varint %s' % str(e))
      else:
        b = buffer[pos]
        pos += 1
      result |= ((b & 0x7f) << shift)
      if not (b & 0x80):
        result &= mask
        result = result_type(result)
        return result if pos is None else (result, pos)
      shift += 7
      if shift >= 64:
        raise _DecodeError('Too many bytes when decoding varint.')

  return DecodeVarint

