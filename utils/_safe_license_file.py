import os

def _safe_license_file(file):
    # XXX: Do we need this after the deprecation discussed in #4892, #4896??
    normalized = os.path.normpath(file).replace(os.sep, "/")
    if "../" in normalized:
        return os.path.basename(normalized)  # Temporarily restore pre PEP639 behaviour
    return normalized

