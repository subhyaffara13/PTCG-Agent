
def _encode_host(host: str, validate_host: bool) -> str:
    """Encode host part of URL."""
    # If the host ends with a digit or contains a colon, its likely
    # an IP address.
    if host and (host[-1].isdigit() or ":" in host):
        raw_ip, sep, zone = host.partition("%")
        # If it looks like an IP, we check with _ip_compressed_version
        # and fall-through if its not an IP address. This is a performance
        # optimization to avoid parsing IP addresses as much as possible
        # because it is orders of magnitude slower than almost any other
        # operation this library does.
        # Might be an IP address, check it
        #
        # IP Addresses can look like:
        # https://datatracker.ietf.org/doc/html/rfc3986#section-3.2.2
        # - 127.0.0.1 (last character is a digit)
        # - 2001:db8::ff00:42:8329 (contains a colon)
        # - 2001:db8::ff00:42:8329%eth0 (contains a colon)
        # - [2001:db8::ff00:42:8329] (contains a colon -- brackets should
        #                             have been removed before it gets here)
        # Rare IP Address formats are not supported per:
        # https://datatracker.ietf.org/doc/html/rfc3986#section-7.4
        #
        # IP parsing is slow, so its wrapped in an LRU
        try:
            ip = ip_address(raw_ip)
        except ValueError:
            pass
        else:
            # These checks should not happen in the
            # LRU to keep the cache size small
            host = ip.compressed
            if ip.version == 6:
                return f"[{host}%{zone}]" if sep else f"[{host}]"
            return f"{host}%{zone}" if sep else host

    # IDNA encoding is slow, skip it for ASCII-only strings
    if host.isascii():
        # Check for invalid characters explicitly; _idna_encode() does this
        # for non-ascii host names.
        host = host.lower()
        if validate_host and (invalid := NOT_REG_NAME.search(host)):
            value, pos, extra = invalid.group(), invalid.start(), ""
            if value == "@" or (value == ":" and "@" in host[pos:]):
                # this looks like an authority string
                extra = (
                    ", if the value includes a username or password, "
                    "use 'authority' instead of 'host'"
                )
            raise ValueError(
                f"Host {host!r} cannot contain {value!r} (at position {pos}){extra}"
            ) from None
        return host

    return _idna_encode(host)

