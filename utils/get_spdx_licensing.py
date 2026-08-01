
def get_spdx_licensing(license_index_location=vendored_scancode_licensedb_index_location):
    """
    Return a Licensing object using SPDX license keys loaded from a
    ``license_index_location`` location of a license db JSON index files
    See https://scancode-licensedb.aboutcode.org/index.json
    """
    return build_spdx_licensing(get_license_index(license_index_location))

