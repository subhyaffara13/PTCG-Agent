import json

def get_license_index(license_index_location=vendored_scancode_licensedb_index_location):
    """
    Return a list of mappings that contain license key information from
    ``license_index_location``

    The default value of `license_index_location` points to a vendored copy
    of the license index from https://scancode-licensedb.aboutcode.org/
    """
    with open(license_index_location) as f:
        return json.load(f)

