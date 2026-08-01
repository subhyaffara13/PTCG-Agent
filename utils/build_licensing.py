
def build_licensing(license_index):
    """
    Return a Licensing object that has been loaded with license keys and
    attributes from a ``license_index`` list of simple ScanCode license mappings.
    """
    lics = [
        {
            "key": l.get("license_key", ""),
            "is_deprecated": l.get("is_deprecated", False),
            "is_exception": l.get("is_exception", False),
        }
        for l in license_index
    ]
    return load_licensing_from_license_index(lics)

