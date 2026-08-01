
def test_encrypt_decrypt_roundtrip():
    data = b'this is my plaintext \0\1\2\3'
    encrypted = t1f.Type1Font._encrypt(data, 'eexec')
    decrypted = t1f.Type1Font._decrypt(encrypted, 'eexec')
    assert encrypted != decrypted
    assert data == decrypted

