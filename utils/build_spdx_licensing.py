
def build_spdx_licensing(license_index):
    """
    Return a Licensing object that has been loaded with license keys and
    attributes from a ``license_index`` list of simple SPDX license mappings.
    """
    # Massage data such that SPDX license key is the primary license key
    lics = [
        {
            "key": l.get("spdx_license_key", ""),
            "aliases": l.get("other_spdx_license_keys", []),
            "is_deprecated": l.get("is_deprecated", False),
            "is_exception": l.get("is_exception", False),
        }
        for l in license_index
        if l.get("spdx_license_key")
    ]
    return load_licensing_from_license_index(lics)

