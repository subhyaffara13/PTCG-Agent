
def _import_riva():
    """
    Lazy import of ``riva.client`` and ``riva.client.proto.riva_asr_pb2``.

    We try the SDK first (preferred) and fall back to importing the proto
    module separately when the SDK packaging changes between versions.
    """
    try:
        import riva.client as riva_client  # type: ignore
    except ImportError as e:
        raise NvidiaRivaException(status_code=500, message=_RIVA_INSTALL_HINT) from e

    riva_asr_module = riva_client
    if not hasattr(riva_asr_module, "RecognitionConfig"):
        try:
            import riva.client.proto.riva_asr_pb2 as riva_asr_pb2  # type: ignore

            riva_asr_module = riva_asr_pb2
        except ImportError as e:
            raise NvidiaRivaException(
                status_code=500, message=_RIVA_INSTALL_HINT
            ) from e

    return riva_client, riva_asr_module

