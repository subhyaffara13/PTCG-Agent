
def get_and_parse_agent_identity_certificate():
    """Gets and parses the agent identity certificate if not opted out.

    Checks if the user has opted out of certificate-bound tokens. If not,
    it gets the certificate path, reads the file, and parses it.

    Returns:
        The parsed certificate object if found and not opted out, otherwise None.
    """
    # If the user has opted out of cert bound tokens, there is no need to
    # look up the certificate.
    is_opted_out = (
        os.environ.get(
            environment_vars.GOOGLE_API_PREVENT_AGENT_TOKEN_SHARING_FOR_GCP_SERVICES,
            "true",
        ).lower()
        == "false"
    )
    if is_opted_out:
        return None

    cert_path = get_agent_identity_certificate_path()
    if not cert_path:
        return None

    with open(cert_path, "rb") as cert_file:
        cert_bytes = cert_file.read()

    return parse_certificate(cert_bytes)

