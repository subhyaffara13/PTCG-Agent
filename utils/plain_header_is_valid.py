
def plain_header_is_valid(header: Header) -> bool:
  plain = header.plain
  keys = [t[1] for t in string.Formatter().parse(plain) if t[1] is not None]
  return 'sender' in keys and 'receiver' in keys

