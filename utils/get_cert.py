
def get_cert(signer_lib, config_file_path):
    # First call to calculate the cert length
    cert_len = signer_lib.GetCertPemForPython(
        config_file_path.encode(),  # configFilePath
        None,  # certHolder
        0,  # certHolderLen
    )
    if cert_len == 0:
        raise exceptions.MutualTLSChannelError("failed to get certificate")

    # Then we create an array to hold the cert, and call again to fill the cert
    cert_holder = ctypes.create_string_buffer(cert_len)
    signer_lib.GetCertPemForPython(
        config_file_path.encode(),  # configFilePath
        cert_holder,  # certHolder
        cert_len,  # certHolderLen
    )
    return bytes(cert_holder)

