
def _legacy_runtime_signature(
    client: BedrockOpenAI | AsyncBedrockOpenAI,
    configuration: _LegacyAuthConfiguration,
) -> _LegacyRuntimeSignature:
    mode, credential = configuration
    credential_identity: object = (
        hashlib.blake2s(credential.encode(), key=_LEGACY_SIGNATURE_KEY).digest()
        if isinstance(credential, str)
        else id(credential)
    )
    return _LegacyRuntimeSignature(
        mode=mode,
        base_url=str(client.base_url),
        region=client.aws_region,
        credential_identity=credential_identity,
    )

