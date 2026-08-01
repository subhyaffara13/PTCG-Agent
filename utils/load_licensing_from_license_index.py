
def load_licensing_from_license_index(license_index):
    """
    Return a Licensing object that has been loaded with license keys and
    attributes from a ``license_index`` list of license mappings.
    """
    syms = [LicenseSymbol(**l) for l in license_index]
    return Licensing(syms)

