
def _get_primary_ip():
  """Returns the primary IP address of the host, preferring IPv4."""
  addrinfos = socket.getaddrinfo(socket.gethostname(), None)
  for family, _, _, _, sockaddr in addrinfos:
    if family in [socket.AF_INET, socket.AF_INET6]:
      return family, sockaddr[0]

  raise ValueError('Failed to detect the primary IP address')

