
def _read_cert_and_key_files(cert_path, key_path):
    cert_data = _read_cert_file(cert_path)
    key_data = _read_key_file(key_path)

    return cert_data, key_data

