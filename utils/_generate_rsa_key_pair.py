
def _generate_rsa_key_pair() -> RSAPrivateKey:
    """Generate a new RSA-2048 private key."""
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

