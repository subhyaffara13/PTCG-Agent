
def _verify_response(issuer_cert, ocsp_response):
    pubkey = issuer_cert.public_key()
    try:
        if isinstance(pubkey, RSAPublicKey):
            pubkey.verify(
                ocsp_response.signature,
                ocsp_response.tbs_response_bytes,
                PKCS1v15(),
                ocsp_response.signature_hash_algorithm,
            )
        elif isinstance(pubkey, DSAPublicKey):
            pubkey.verify(
                ocsp_response.signature,
                ocsp_response.tbs_response_bytes,
                ocsp_response.signature_hash_algorithm,
            )
        elif isinstance(pubkey, EllipticCurvePublicKey):
            pubkey.verify(
                ocsp_response.signature,
                ocsp_response.tbs_response_bytes,
                ECDSA(ocsp_response.signature_hash_algorithm),
            )
        else:
            pubkey.verify(ocsp_response.signature, ocsp_response.tbs_response_bytes)
    except InvalidSignature:
        raise ConnectionError("failed to valid ocsp response")

