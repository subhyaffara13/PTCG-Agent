import re

def _read_key_file(key_path):
    with open(key_path, "rb") as key_file:
        key_data = key_file.read()

    key_match = re.findall(_KEY_REGEX, key_data)
    if len(key_match) != 1:
        raise exceptions.ClientCertError(
            "Private key file {} is in an invalid format, a single PEM formatted private key is expected".format(
                key_path
            )
        )

    return key_match[0]

