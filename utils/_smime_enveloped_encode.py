
def _smime_enveloped_encode(data: bytes) -> bytes:
    m = email.message.Message()
    m.add_header("MIME-Version", "1.0")
    m.add_header("Content-Disposition", "attachment", filename="smime.p7m")
    m.add_header(
        "Content-Type",
        "application/pkcs7-mime",
        smime_type="enveloped-data",
        name="smime.p7m",
    )
    m.add_header("Content-Transfer-Encoding", "base64")

    m.set_payload(email.base64mime.body_encode(data, maxlinelen=65))

    return m.as_bytes(policy=m.policy.clone(linesep="\n", max_line_length=0))

