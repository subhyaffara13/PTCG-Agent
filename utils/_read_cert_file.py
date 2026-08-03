import re

def _read_cert_file(cert_path):
    with open(cert_path, "rb") as cert_file:
        cert_data = cert_file.read()

    cert_match = re.findall(_CERT_REGEX, cert_data)
    if len(cert_match) != 1:
        raise exceptions.ClientCertError(
            "Certificate file {} is in an invalid format, a single PEM formatted certificate is expected".format(
                cert_path
            )
        )
    return cert_match[0]

