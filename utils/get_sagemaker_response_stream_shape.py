
def get_sagemaker_response_stream_shape():
    """
    Lazily load and cache the sagemaker-runtime stream shape for the process.

    Avoids importing botocore (and logging warnings) unless SageMaker event-stream
    decoding is actually needed.
    """
    return _load_sagemaker_response_stream_shape()

