
def ssh_key_fingerprint(
    key: SSHPublicKeyTypes,
    hash_algorithm: hashes.MD5 | hashes.SHA256,
) -> bytes:
    if not isinstance(hash_algorithm, (hashes.MD5, hashes.SHA256)):
        raise TypeError("hash_algorithm must be either MD5 or SHA256")

    key_type = _get_ssh_key_type(key)
    kformat = _lookup_kformat(key_type)

    f_pub = _FragList()
    f_pub.put_sshstr(key_type)
    kformat.encode_public(key, f_pub)

    ssh_binary_data = f_pub.tobytes()

    # Hash the binary data
    hash_obj = hashes.Hash(hash_algorithm)
    hash_obj.update(ssh_binary_data)
    return hash_obj.finalize()

