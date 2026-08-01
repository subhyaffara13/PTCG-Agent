
def unregister_encoder(encoder: Encoder) -> None:
    """Unregister a custom encoder."""
    with contextlib.suppress(ValueError):
        CUSTOM_ENCODERS.remove(encoder)

