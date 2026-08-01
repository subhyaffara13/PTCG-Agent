
def encode_host(host: str) -> str:
    if not host:
        return ""

    elif IPv4_STYLE_HOSTNAME.match(host):
        # Validate IPv4 hostnames like #.#.#.#
        #
        # From https://datatracker.ietf.org/doc/html/rfc3986/#section-3.2.2
        #
        # IPv4address = dec-octet "." dec-octet "." dec-octet "." dec-octet
        try:
            ipaddress.IPv4Address(host)
        except ipaddress.AddressValueError:
            raise InvalidURL(f"Invalid IPv4 address: {host!r}")
        return host

    elif IPv6_STYLE_HOSTNAME.match(host):
        # Validate IPv6 hostnames like [...]
        #
        # From https://datatracker.ietf.org/doc/html/rfc3986/#section-3.2.2
        #
        # "A host identified by an Internet Protocol literal address, version 6
        # [RFC3513] or later, is distinguished by enclosing the IP literal
        # within square brackets ("[" and "]").  This is the only place where
        # square bracket characters are allowed in the URI syntax."
        try:
            ipaddress.IPv6Address(host[1:-1])
        except ipaddress.AddressValueError:
            raise InvalidURL(f"Invalid IPv6 address: {host!r}")
        return host[1:-1]

    elif host.isascii():
        # Regular ASCII hostnames
        #
        # From https://datatracker.ietf.org/doc/html/rfc3986/#section-3.2.2
        #
        # reg-name    = *( unreserved / pct-encoded / sub-delims )
        WHATWG_SAFE = '"`{}%|\\'
        return quote(host.lower(), safe=SUB_DELIMS + WHATWG_SAFE)

    # IDNA hostnames
    try:
        return idna.encode(host.lower()).decode("ascii")
    except idna.IDNAError:
        raise InvalidURL(f"Invalid IDNA hostname: {host!r}")

