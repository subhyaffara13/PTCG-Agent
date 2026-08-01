
def _ipaddress_match(ipname: str, host_ip: IPv4Address | IPv6Address) -> bool:
    """Exact matching of IP addresses.

    RFC 9110 section 4.3.5: "A reference identity of IP-ID contains the decoded
    bytes of the IP address. An IP version 4 address is 4 octets, and an IP
    version 6 address is 16 octets. [...] A reference identity of type IP-ID
    matches if the address is identical to an iPAddress value of the
    subjectAltName extension of the certificate."
    """
    # OpenSSL may add a trailing newline to a subjectAltName's IP address
    # Divergence from upstream: ipaddress can't handle byte str
    ip = ipaddress.ip_address(ipname.rstrip())
    return bool(ip.packed == host_ip.packed)


def _ipaddress_match(ipname: str, host_ip: IPv4Address | IPv6Address) -> bool:
    """Exact matching of IP addresses.

    RFC 9110 section 4.3.5: "A reference identity of IP-ID contains the decoded
    bytes of the IP address. An IP version 4 address is 4 octets, and an IP
    version 6 address is 16 octets. [...] A reference identity of type IP-ID
    matches if the address is identical to an iPAddress value of the
    subjectAltName extension of the certificate."
    """
    # OpenSSL may add a trailing newline to a subjectAltName's IP address
    # Divergence from upstream: ipaddress can't handle byte str
    ip = ipaddress.ip_address(ipname.rstrip())
    return bool(ip.packed == host_ip.packed)

