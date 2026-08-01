
def _load_sagemaker_response_stream_shape():
    try:
        from botocore.loaders import Loader
        from botocore.model import ServiceModel

        loader = Loader()
        service_dict = loader.load_service_model("sagemaker-runtime", "service-2")
        return ServiceModel(service_dict).shape_for(
            "InvokeEndpointWithResponseStreamOutput"
        )
    except Exception as e:
        verbose_logger.warning(
            "litellm: could not load sagemaker-runtime response stream shape "
            "— SageMaker event-stream decoding will be unavailable. Error: %s",
            e,
        )
        return None

