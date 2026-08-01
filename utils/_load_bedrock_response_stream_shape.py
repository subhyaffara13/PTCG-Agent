
def _load_bedrock_response_stream_shape():
    """
    Load the ResponseStream shape from botocore's bundled bedrock-runtime schema.

    Returns ``None`` if botocore is unavailable or the service model cannot be
    loaded.
    """
    try:
        from botocore.loaders import Loader
        from botocore.model import ServiceModel

        loader = Loader()
        service_dict = loader.load_service_model("bedrock-runtime", "service-2")
        return ServiceModel(service_dict).shape_for("ResponseStream")
    except Exception as e:
        verbose_logger.warning(
            "litellm: could not load bedrock-runtime response stream shape "
            "— Bedrock event-stream decoding will be unavailable. Error: %s",
            e,
        )
        return None

