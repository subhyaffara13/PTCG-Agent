
def _strip_addresses(addresses, prefix):
  return ','.join([_strip_prefix(s, prefix) for s in addresses.split(',')])

