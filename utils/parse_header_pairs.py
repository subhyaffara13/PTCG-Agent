
def parse_header_pairs(header: str) -> dict[str, str]:
    """
    Parse key-value pairs from WWW-Authenticate or similar HTTP headers.

    This function handles the complex format of WWW-Authenticate header values,
    supporting both quoted and unquoted values, proper handling of commas in
    quoted values, and whitespace variations per RFC 7616.

    Examples of supported formats:
      - key1="value1", key2=value2
      - key1 = "value1" , key2="value, with, commas"
      - key1=value1,key2="value2"
      - realm="example.com", nonce="12345", qop="auth"

    Args:
        header: The header value string to parse

    Returns:
        Dictionary mapping parameter names to their values
    """
    return {
        stripped_key: unescape_quotes(quoted_val) if quoted_val else unquoted_val
        for key, quoted_val, unquoted_val in _HEADER_PAIRS_PATTERN.findall(header)
        if (stripped_key := key.strip())
    }

