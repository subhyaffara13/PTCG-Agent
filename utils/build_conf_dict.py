
def build_conf_dict(name, bid, cwe, qualnames, message, level="MEDIUM"):
    """Build and return a blacklist configuration dict."""
    return {
        "name": name,
        "id": bid,
        "cwe": cwe,
        "message": message,
        "qualnames": qualnames,
        "level": level,
    }

