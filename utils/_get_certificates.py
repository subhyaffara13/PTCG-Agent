
def _get_certificates(certs, issuer_cert, responder_name, responder_hash):
    if responder_name is None:
        certificates = [
            c
            for c in certs
            if _get_pubkey_hash(c) == responder_hash and c.issuer == issuer_cert.subject
        ]
    else:
        certificates = [
            c
            for c in certs
            if c.subject == responder_name and c.issuer == issuer_cert.subject
        ]

    return certificates

